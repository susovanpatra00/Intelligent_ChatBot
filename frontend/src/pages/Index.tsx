import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Message, ChatOption } from '../types/chat';
import ChatHeader from '../components/ChatHeader';
import ChatContainer from '../components/ChatContainer';
import ChatInput from '../components/ChatInput';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  // Mock API call - in a real app, this would call your backend
  const sendMessageToBackend = async (content: string, option: ChatOption) => {
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:5001/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: content,
          reasoning: option === "reasoning",
          web: option === "web-search"
        }),
      });

      if (!res.ok) throw new Error("API error");

      const data = await res.json();
      const finalAnswer = data.final || "No response generated.";

      const botMessage: Message = {
        id: uuidv4(),
        content: finalAnswer,
        sender: 'bot',
        timestamp: new Date(),
        sources: data.sources || [],  // 👈 Add this
      };


      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to get response from server.",
        variant: "destructive",
      });
      console.error("Backend error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = (content: string, option: ChatOption) => {
    const userMessage: Message = {
      id: uuidv4(),
      content,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    sendMessageToBackend(content, option);
  };

  const handleLike = (messageId: string) => {
    setMessages(prev =>
      prev.map(msg => {
        if (msg.id === messageId) {
          // If already liked, remove the like
          if (msg.liked) {
            return { ...msg, liked: false, disliked: false, feedbackGiven: false };
          }
          // Otherwise set it to liked
          return { ...msg, liked: true, disliked: false, feedbackGiven: true };
        }
        return msg;
      })
    );

    toast({
      title: "Thank you!",
      description: "Your feedback has been recorded.",
    });
  };

  const handleDislike = (messageId: string) => {
    setMessages(prev =>
      prev.map(msg => {
        if (msg.id === messageId) {
          // If already disliked, remove the dislike
          if (msg.disliked) {
            return { ...msg, liked: false, disliked: false, feedbackGiven: false };
          }
          // Otherwise set it to disliked
          return { ...msg, liked: false, disliked: true, feedbackGiven: true };
        }
        return msg;
      })
    );

    toast({
      title: "Feedback received",
      description: "We'll use your feedback to improve.",
    });
  };

  return (
    <div className="min-h-screen flex flex-col">
      <ChatHeader />

      <main className="flex-1 flex flex-col max-w-5xl w-full mx-auto px-4 sm:px-6 py-4">
        <div className="flex-1 flex flex-col rounded-xl overflow-hidden shadow-sm">
          <ChatContainer
            messages={messages}
            isLoading={isLoading}
            onLike={handleLike}
            onDislike={handleDislike}
          />
          <div className="p-4">
            <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;