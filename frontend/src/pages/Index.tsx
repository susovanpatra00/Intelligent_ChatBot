// Version: 0.0
// import React, { useState } from 'react';
// import { v4 as uuidv4 } from 'uuid';
// import { Message, ChatOption } from '../types/chat';
// import ChatHeader from '../components/ChatHeader';
// import ChatContainer from '../components/ChatContainer';
// import ChatInput from '../components/ChatInput';
// import { useToast } from '@/hooks/use-toast';

// const Index = () => {
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const { toast } = useToast();

//   // Mock API call - in a real app, this would call your backend
//   const sendMessageToBackend = async (content: string, option: ChatOption) => {
//     setIsLoading(true);

//     try {
//       // In a real implementation, this would be an API call
//       // Simulating network delay
//       await new Promise(resolve => setTimeout(resolve, 1500));

//       // Example response with markdown
//       let response: string;

//       if (option === 'reasoning') {
//         response = `**Reasoning Mode**: I'm analyzing your query step by step.\n\n
// Here's my thought process:
// 1. First, I considered the key points in your message
// 2. Then, I evaluated different perspectives
// 3. Finally, I reached a conclusion based on logical analysis

// This is *formatted markdown* with:
// - Bullet points
// - **Bold text**
// - *Italic text*
// - \`code snippets\`

// > And even blockquotes for emphasis!`;
//       } else if (option === 'web-search') {
//         response = `**Web Search Results**\n\n
// According to recent sources:

// | Source | Information |
// |--------|-------------|
// | Wikipedia | Provides general overview |
// | Research journals | Offers detailed analysis |
// | News outlets | Covers recent developments |

// You can learn more by visiting [example link](https://example.com).

// \`\`\`
// // Even code blocks work!
// function example() {
//   return "Hello world";
// }
// \`\`\``;
//       } else {
//         response = `I'm processing your message: "${content}"\n\nThis is a standard response with some **bold text** and *italic text* to demonstrate markdown formatting.`;
//       }

//       const botMessage: Message = {
//         id: uuidv4(),
//         content: response,
//         sender: 'bot',
//         timestamp: new Date(),
//       };

//       setMessages(prev => [...prev, botMessage]);
//     } catch (error) {
//       toast({
//         title: "Error",
//         description: "Failed to send message. Please try again.",
//         variant: "destructive",
//       });
//       console.error("Error sending message:", error);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleSendMessage = (content: string, option: ChatOption) => {
//     const userMessage: Message = {
//       id: uuidv4(),
//       content,
//       sender: 'user',
//       timestamp: new Date(),
//     };

//     setMessages(prev => [...prev, userMessage]);
//     sendMessageToBackend(content, option);
//   };

//   const handleLike = (messageId: string) => {
//     setMessages(prev => 
//       prev.map(msg => {
//         if (msg.id === messageId) {
//           // If already liked, remove the like
//           if (msg.liked) {
//             return { ...msg, liked: false, disliked: false, feedbackGiven: false };
//           }
//           // Otherwise set it to liked
//           return { ...msg, liked: true, disliked: false, feedbackGiven: true };
//         }
//         return msg;
//       })
//     );

//     toast({
//       title: "Thank you!",
//       description: "Your feedback has been recorded.",
//     });
//   };

//   const handleDislike = (messageId: string) => {
//     setMessages(prev => 
//       prev.map(msg => {
//         if (msg.id === messageId) {
//           // If already disliked, remove the dislike
//           if (msg.disliked) {
//             return { ...msg, liked: false, disliked: false, feedbackGiven: false };
//           }
//           // Otherwise set it to disliked
//           return { ...msg, liked: false, disliked: true, feedbackGiven: true };
//         }
//         return msg;
//       })
//     );

//     toast({
//       title: "Feedback received",
//       description: "We'll use your feedback to improve.",
//     });
//   };

//   return (
//     <div className="min-h-screen flex flex-col bg-gray-50">
//       <ChatHeader />

//       <main className="flex-1 flex flex-col max-w-5xl w-full mx-auto px-4 sm:px-6 py-4">
//         <div className="flex-1 flex flex-col border border-gray-200 rounded-xl overflow-hidden shadow-sm bg-white">
//           <ChatContainer 
//             messages={messages} 
//             isLoading={isLoading} 
//             onLike={handleLike} 
//             onDislike={handleDislike} 
//           />
//           <div className="p-4 border-t border-gray-200">
//             <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
//           </div>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default Index;
//////////////////////////////////////////////////////////////////////////////////////////////





// Version 0.0
// import React, { useState } from 'react';
// import { v4 as uuidv4 } from 'uuid';
// import { Message, ChatOption } from '../types/chat';
// import ChatHeader from '../components/ChatHeader';
// import ChatContainer from '../components/ChatContainer';
// import ChatInput from '../components/ChatInput';
// import { useToast } from '@/hooks/use-toast';

// const Index = () => {
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const { toast } = useToast();

//   // Mock API call - in a real app, this would call your backend
//   const sendMessageToBackend = async (content: string, option: ChatOption) => {
//     setIsLoading(true);

//     try {
//       const res = await fetch("http://localhost:5001/chat", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           query: content,
//           reasoning: option === "reasoning",
//           web: option === "web-search"
//         }),
//       });

//       if (!res.ok) throw new Error("API error");

//       const data = await res.json();
//       const finalAnswer = data.final || "No response generated.";

//       const botMessage: Message = {
//         id: uuidv4(),
//         content: finalAnswer,
//         sender: 'bot',
//         timestamp: new Date(),
//       };

//       setMessages(prev => [...prev, botMessage]);

//     } catch (error) {
//       toast({
//         title: "Error",
//         description: "Failed to get response from server.",
//         variant: "destructive",
//       });
//       console.error("Backend error:", error);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleSendMessage = (content: string, option: ChatOption) => {
//     const userMessage: Message = {
//       id: uuidv4(),
//       content,
//       sender: 'user',
//       timestamp: new Date(),
//     };

//     setMessages(prev => [...prev, userMessage]);
//     sendMessageToBackend(content, option);
//   };

//   const handleLike = (messageId: string) => {
//     setMessages(prev =>
//       prev.map(msg => {
//         if (msg.id === messageId) {
//           // If already liked, remove the like
//           if (msg.liked) {
//             return { ...msg, liked: false, disliked: false, feedbackGiven: false };
//           }
//           // Otherwise set it to liked
//           return { ...msg, liked: true, disliked: false, feedbackGiven: true };
//         }
//         return msg;
//       })
//     );

//     toast({
//       title: "Thank you!",
//       description: "Your feedback has been recorded.",
//     });
//   };

//   const handleDislike = (messageId: string) => {
//     setMessages(prev =>
//       prev.map(msg => {
//         if (msg.id === messageId) {
//           // If already disliked, remove the dislike
//           if (msg.disliked) {
//             return { ...msg, liked: false, disliked: false, feedbackGiven: false };
//           }
//           // Otherwise set it to disliked
//           return { ...msg, liked: false, disliked: true, feedbackGiven: true };
//         }
//         return msg;
//       })
//     );

//     toast({
//       title: "Feedback received",
//       description: "We'll use your feedback to improve.",
//     });
//   };

//   return (
//     <div className="min-h-screen flex flex-col bg-gray-50">
//       <ChatHeader />

//       <main className="flex-1 flex flex-col max-w-5xl w-full mx-auto px-4 sm:px-6 py-4">
//         <div className="flex-1 flex flex-col border border-gray-200 rounded-xl overflow-hidden shadow-sm bg-white">
//           <ChatContainer
//             messages={messages}
//             isLoading={isLoading}
//             onLike={handleLike}
//             onDislike={handleDislike}
//           />
//           <div className="p-4 border-t border-gray-200">
//             <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
//           </div>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default Index;



























// // Version 1.0
// import React, { useState } from 'react';
// import { v4 as uuidv4 } from 'uuid';
// import { Message, ChatOption } from '../types/chat';
// import ChatHeader from '../components/ChatHeader';
// import ChatContainer from '../components/ChatContainer';
// import ChatInput from '../components/ChatInput';
// import { useToast } from '@/hooks/use-toast';

// const Index = () => {
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const { toast } = useToast();

//   // Mock API call - in a real app, this would call your backend
//   const sendMessageToBackend = async (content: string, option: ChatOption) => {
//     setIsLoading(true);

//     try {
//       const res = await fetch("http://localhost:5001/chat", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           query: content,
//           reasoning: option === "reasoning",
//           web: option === "web-search"
//         }),
//       });

//       if (!res.ok) throw new Error("API error");

//       const data = await res.json();
//       const finalAnswer = data.final || "No response generated.";

//       const botMessage: Message = {
//         id: uuidv4(),
//         content: finalAnswer,
//         sender: 'bot',
//         timestamp: new Date(),
//         sources: data.sources || [],  // 👈 Add this
//       };


//       setMessages(prev => [...prev, botMessage]);

//     } catch (error) {
//       toast({
//         title: "Error",
//         description: "Failed to get response from server.",
//         variant: "destructive",
//       });
//       console.error("Backend error:", error);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleSendMessage = (content: string, option: ChatOption) => {
//     const userMessage: Message = {
//       id: uuidv4(),
//       content,
//       sender: 'user',
//       timestamp: new Date(),
//     };

//     setMessages(prev => [...prev, userMessage]);
//     sendMessageToBackend(content, option);
//   };

//   const handleLike = (messageId: string) => {
//     setMessages(prev =>
//       prev.map(msg => {
//         if (msg.id === messageId) {
//           // If already liked, remove the like
//           if (msg.liked) {
//             return { ...msg, liked: false, disliked: false, feedbackGiven: false };
//           }
//           // Otherwise set it to liked
//           return { ...msg, liked: true, disliked: false, feedbackGiven: true };
//         }
//         return msg;
//       })
//     );

//     toast({
//       title: "Thank you!",
//       description: "Your feedback has been recorded.",
//     });
//   };

//   const handleDislike = (messageId: string) => {
//     setMessages(prev =>
//       prev.map(msg => {
//         if (msg.id === messageId) {
//           // If already disliked, remove the dislike
//           if (msg.disliked) {
//             return { ...msg, liked: false, disliked: false, feedbackGiven: false };
//           }
//           // Otherwise set it to disliked
//           return { ...msg, liked: false, disliked: true, feedbackGiven: true };
//         }
//         return msg;
//       })
//     );

//     toast({
//       title: "Feedback received",
//       description: "We'll use your feedback to improve.",
//     });
//   };

//   return (
//     <div className="min-h-screen flex flex-col bg-gray-50">
//       <ChatHeader />

//       <main className="flex-1 flex flex-col max-w-5xl w-full mx-auto px-4 sm:px-6 py-4">
//         <div className="flex-1 flex flex-col border border-gray-200 rounded-xl overflow-hidden shadow-sm bg-white">
//           <ChatContainer
//             messages={messages}
//             isLoading={isLoading}
//             onLike={handleLike}
//             onDislike={handleDislike}
//           />
//           <div className="p-4 border-t border-gray-200">
//             <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
//           </div>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default Index;










// Version 1.0
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
    // 1. Call your query rewriting API or function here
    // 1. Call your query rewriting API or function here
    let rewrittenQuery = content; // default fallback

    try {
      const rewriteRes = await fetch("http://localhost:5001/rewrite_query", {  // your query rewriting endpoint
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: content, conversation: messages }), // send previous messages for context
      });
      if (rewriteRes.ok) {
        const rewriteData = await rewriteRes.json();
        rewrittenQuery = rewriteData.rewrittenQuery || content;
      }
    } catch (err) {
      console.warn("Query rewrite failed, using original query");
    }

    // 2. Use rewrittenQuery instead of content for backend chat call


    try {
      const res = await fetch("http://localhost:5001/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          // query: content,
          query: rewrittenQuery,
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
