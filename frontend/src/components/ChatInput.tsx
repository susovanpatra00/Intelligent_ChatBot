// // Version: 0.0
// // import React, { useState } from 'react';
// // import { Button } from '@/components/ui/button';
// // import { Textarea } from '@/components/ui/textarea';
// // import { ChatOption } from '../types/chat';
// // import { SendIcon, RefreshCw, Search } from 'lucide-react';

// // interface ChatInputProps {
// //   onSendMessage: (content: string, option: ChatOption) => void;
// //   isLoading: boolean;
// // }

// // const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
// //   const [message, setMessage] = useState('');
// //   const [selectedOption, setSelectedOption] = useState<ChatOption>(null);

// //   const handleSend = () => {
// //     if (message.trim() && !isLoading) {
// //       onSendMessage(message, selectedOption);
// //       setMessage('');
// //     }
// //   };

// //   const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
// //     if (e.key === 'Enter' && !e.shiftKey) {
// //       e.preventDefault();
// //       handleSend();
// //     }
// //   };

// //   const toggleOption = (option: ChatOption) => {
// //     setSelectedOption(prev => prev === option ? null : option);
// //   };

// //   return (
// //     <div className="border border-gray-200 rounded-xl p-3 bg-white shadow-sm">
// //       <Textarea
// //         placeholder="Type your message..."
// //         className="min-h-[80px] resize-none border-0 focus-visible:ring-0 focus-visible:ring-offset-0 p-2"
// //         value={message}
// //         onChange={(e) => setMessage(e.target.value)}
// //         onKeyDown={handleKeyDown}
// //         disabled={isLoading}
// //       />
// //       <div className="flex items-center justify-between pt-3 border-t border-gray-200">
// //         <div className="flex gap-2">
// //           <Button
// //             variant="outline"
// //             size="sm"
// //             className={`flex items-center gap-1 text-xs ${selectedOption === 'reasoning'
// //                 ? 'bg-chat-red text-white hover:bg-chat-red hover:text-white'
// //                 : 'hover:bg-chat-red/10 hover:text-chat-red'
// //               }`}
// //             onClick={() => toggleOption('reasoning')}
// //             type="button"
// //           >
// //             <RefreshCw className="w-3.5 h-3.5" />
// //             Reasoning
// //           </Button>
// //           <Button
// //             variant="outline"
// //             size="sm"
// //             className={`flex items-center gap-1 text-xs ${selectedOption === 'web-search'
// //                 ? 'bg-chat-red text-white hover:bg-chat-red hover:text-white'
// //                 : 'hover:bg-chat-red/10 hover:text-chat-red'
// //               }`}
// //             onClick={() => toggleOption('web-search')}
// //             type="button"
// //           >
// //             <Search className="w-3.5 h-3.5" />
// //             Web-Search
// //           </Button>
// //         </div>
// //         <Button
// //           onClick={handleSend}
// //           disabled={!message.trim() || isLoading}
// //           className="bg-chat-red hover:bg-chat-red-dark text-white"
// //           size="sm"
// //         >
// //           {isLoading ? (
// //             <RefreshCw className="w-4 h-4 animate-spin" />
// //           ) : (
// //             <>
// //               <span className="mr-1">Send</span>
// //               <SendIcon className="w-4 h-4" />
// //             </>
// //           )}
// //         </Button>
// //       </div>
// //     </div>
// //   );
// // };

// // export default ChatInput;










// // Version: 1.0
// // import React, { useState } from 'react';
// // import { Mic, MicOff } from 'lucide-react';
// // import { Button } from '@/components/ui/button';
// // import { Textarea } from '@/components/ui/textarea';
// // import { ChatOption } from '../types/chat';
// // import { SendIcon, RefreshCw, Search } from 'lucide-react';

// // interface ChatInputProps {
// //   onSendMessage: (content: string, option: ChatOption) => void;
// //   isLoading: boolean;
// // }

// // const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
// //   const [message, setMessage] = useState('');
// //   const [selectedOption, setSelectedOption] = useState<ChatOption>(null);
// //   const [listening, setListening] = useState(false);


// //   const handleSend = () => {
// //     if (message.trim() && !isLoading) {
// //       onSendMessage(message, selectedOption);
// //       setMessage('');
// //     }
// //   };

// //   const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
// //     if (e.key === 'Enter' && !e.shiftKey) {
// //       e.preventDefault();
// //       handleSend();
// //     }
// //   };

// //   const toggleOption = (option: ChatOption) => {
// //     setSelectedOption(prev => prev === option ? null : option);
// //   };

// //   const startVoiceRecognition = () => {
// //     const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
// //     if (!SpeechRecognition) {
// //       alert("Your browser doesn't support speech recognition.");
// //       return;
// //     }

// //     const recognition = new SpeechRecognition();
// //     recognition.lang = 'en-IN';
// //     recognition.interimResults = false;
// //     recognition.maxAlternatives = 1;

// //     recognition.onstart = () => setListening(true);
// //     recognition.onend = () => setListening(false);
// //     recognition.onerror = (e: any) => {
// //       setListening(false);
// //       console.error("Voice error:", e);
// //     };

// //     recognition.onresult = (event: any) => {
// //       const transcript = event.results[0][0].transcript;
// //       setMessage(transcript);
// //     };

// //     recognition.start();
// //   };


// //   return (
// //     <div className="border border-gray-200 rounded-xl p-3 bg-white shadow-sm">
// //       <Textarea
// //         placeholder="Ask your query..."
// //         className="min-h-[80px] resize-none border-0 focus-visible:ring-0 focus-visible:ring-offset-0 p-2"
// //         value={message}
// //         onChange={(e) => setMessage(e.target.value)}
// //         onKeyDown={handleKeyDown}
// //         disabled={isLoading}
// //       />
// //       <div className="flex items-center justify-between pt-3 border-t border-gray-200">
// //         <div className="flex gap-2">
// //           <Button
// //             variant="outline"
// //             size="sm"
// //             className={`flex items-center gap-1 text-xs ${selectedOption === 'reasoning'
// //               ? 'bg-chat-red text-white hover:bg-chat-red hover:text-white'
// //               : 'hover:bg-chat-red/10 hover:text-chat-red'
// //               }`}
// //             onClick={() => toggleOption('reasoning')}
// //             type="button"
// //           >
// //             <RefreshCw className="w-3.5 h-3.5" />
// //             Reasoning
// //           </Button>
// //           <Button
// //             variant="outline"
// //             size="sm"
// //             className={`flex items-center gap-1 text-xs ${selectedOption === 'web-search'
// //               ? 'bg-chat-red text-white hover:bg-chat-red hover:text-white'
// //               : 'hover:bg-chat-red/10 hover:text-chat-red'
// //               }`}
// //             onClick={() => toggleOption('web-search')}
// //             type="button"
// //           >
// //             <Search className="w-3.5 h-3.5" />
// //             Web-Search
// //           </Button>
// //           <Button
// //             variant="outline"
// //             size="sm"
// //             className="flex items-center gap-1 text-xs hover:bg-chat-red/10 hover:text-chat-red"
// //             onClick={startVoiceRecognition}
// //             type="button"
// //           >
// //             {listening ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5" />}
// //             {listening ? "Listening..." : "Speak"}
// //           </Button>
// //         </div>
// //         <Button
// //           onClick={handleSend}
// //           disabled={!message.trim() || isLoading}
// //           className="bg-chat-red hover:bg-chat-red-dark text-white"
// //           size="sm"
// //         >
// //           {isLoading ? (
// //             <RefreshCw className="w-4 h-4 animate-spin" />
// //           ) : (
// //             <>
// //               <span className="mr-1">Send</span>
// //               <SendIcon className="w-4 h-4" />
// //             </>
// //           )}
// //         </Button>
// //       </div>
// //     </div>
// //   );
// // };

// // export default ChatInput;
























// Version: 1.0
// import React, { useState } from 'react';
// import { Mic, MicOff } from 'lucide-react';
// import { Button } from '@/components/ui/button';
// import { Textarea } from '@/components/ui/textarea';
// import { ChatOption } from '../types/chat';
// import { SendIcon, RefreshCw, Search } from 'lucide-react';

// interface ChatInputProps {
//   onSendMessage: (content: string, option: ChatOption) => void;
//   isLoading: boolean;
// }

// const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
//   const [message, setMessage] = useState('');
//   const [selectedOption, setSelectedOption] = useState<ChatOption>(null);
//   const [listening, setListening] = useState(false);


//   const handleSend = () => {
//     if (message.trim() && !isLoading) {
//       onSendMessage(message, selectedOption);
//       setMessage('');
//     }
//   };

//   const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       handleSend();
//     }
//   };

//   const toggleOption = (option: ChatOption) => {
//     setSelectedOption(prev => prev === option ? null : option);
//   };

//   const startVoiceRecognition = () => {
//     const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
//     if (!SpeechRecognition) {
//       alert("Your browser doesn't support speech recognition.");
//       return;
//     }

//     const recognition = new SpeechRecognition();
//     recognition.lang = 'en-IN';
//     recognition.interimResults = false;
//     recognition.maxAlternatives = 1;

//     recognition.onstart = () => setListening(true);
//     recognition.onend = () => setListening(false);
//     recognition.onerror = (e: any) => {
//       setListening(false);
//       console.error("Voice error:", e);
//     };

//     recognition.onresult = (event: any) => {
//       const transcript = event.results[0][0].transcript;
//       setMessage(transcript);
//     };

//     recognition.start();
//   };


//   return (
//     <div className="border border-2 border-[rgba(var(--border-color-rgb),0.5)] rounded-xl p-3 shadow-sm">
//       <Textarea
//         placeholder="Ask your query..."
//         className="min-h-[80px] resize-none border-0 focus-visible:ring-0 focus-visible:ring-offset-0 p-2"
//         value={message}
//         onChange={(e) => setMessage(e.target.value)}
//         onKeyDown={handleKeyDown}
//         disabled={isLoading}
//       />
//       <div className="flex items-center justify-between pt-3 border-t border-gray-200">
//         <div className="flex gap-2">
//           <Button
//             variant="outline"
//             size="sm"
//             className={`flex items-center gap-1 text-xs ${selectedOption === 'reasoning'
//               ? 'bg-chat-red text-white hover:bg-chat-red hover:text-white'
//               : 'hover:bg-chat-red/10 hover:text-chat-red'
//               }`}
//             onClick={() => toggleOption('reasoning')}
//             type="button"
//           >
//             <RefreshCw className="w-3.5 h-3.5" />
//             Reasoning
//           </Button>
//           <Button
//             variant="outline"
//             size="sm"
//             className={`flex items-center gap-1 text-xs ${selectedOption === 'web-search'
//               ? 'bg-chat-red text-white hover:bg-chat-red hover:text-white'
//               : 'hover:bg-chat-red/10 hover:text-chat-red'
//               }`}
//             onClick={() => toggleOption('web-search')}
//             type="button"
//           >
//             <Search className="w-3.5 h-3.5" />
//             Web-Search
//           </Button>
//           <Button
//             variant="outline"
//             size="sm"
//             className="flex items-center gap-1 text-xs hover:bg-chat-red/10 hover:text-chat-red"
//             onClick={startVoiceRecognition}
//             type="button"
//           >
//             {listening ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5" />}
//             {listening ? "Listening..." : "Speak"}
//           </Button>
//         </div>
//         <Button
//           onClick={handleSend}
//           disabled={!message.trim() || isLoading}
//           className="bg-chat-red hover:bg-chat-red-dark text-white"
//           size="sm"
//         >
//           {isLoading ? (
//             <RefreshCw className="w-4 h-4 animate-spin" />
//           ) : (
//             <>
//               <span className="mr-1">Send</span>
//               <SendIcon className="w-4 h-4" />
//             </>
//           )}
//         </Button>
//       </div>
//     </div>
//   );
// };

// export default ChatInput;




Version: 1.0
import React, { useState } from 'react';
import { Mic, MicOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { ChatOption } from '../types/chat';
import { SendIcon, RefreshCw, Search } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (content: string, option: ChatOption) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  const [selectedOption, setSelectedOption] = useState<ChatOption>(null);
  const [listening, setListening] = useState(false);


  const handleSend = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message, selectedOption);
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const toggleOption = (option: ChatOption) => {
    setSelectedOption(prev => prev === option ? null : option);
  };

  const startVoiceRecognition = () => {
    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser doesn't support speech recognition.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);
    recognition.onerror = (e: any) => {
      setListening(false);
      console.error("Voice error:", e);
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setMessage(transcript);
    };

    recognition.start();
  };


  return (
    <div className="border border-2 border-[rgba(var(--border-color-rgb),0.5)] rounded-xl p-3 shadow-sm">
      <Textarea
        placeholder="Ask your query..."
        className="min-h-[80px] resize-none border-0 focus-visible:ring-0 focus-visible:ring-offset-0 p-2"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isLoading}
      />
      <div className="flex items-center justify-between pt-3 border-t border-gray-200">
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className={`flex items-center gap-1 text-xs ${selectedOption === 'reasoning'
              ? 'bg-chat-red text-white hover:bg-chat-red hover:text-white'
              : 'hover:bg-chat-red/10 hover:text-chat-red'
              }`}
            onClick={() => toggleOption('reasoning')}
            type="button"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Reasoning
          </Button>
          <Button
            variant="outline"
            size="sm"
            className={`flex items-center gap-1 text-xs ${selectedOption === 'web-search'
              ? 'bg-chat-red text-white hover:bg-chat-red hover:text-white'
              : 'hover:bg-chat-red/10 hover:text-chat-red'
              }`}
            onClick={() => toggleOption('web-search')}
            type="button"
          >
            <Search className="w-3.5 h-3.5" />
            Web-Search
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="flex items-center gap-1 text-xs hover:bg-chat-red/10 hover:text-chat-red"
            onClick={startVoiceRecognition}
            type="button"
          >
            {listening ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5" />}
            {listening ? "Listening..." : "Speak"}
          </Button>
        </div>
        <Button
          onClick={handleSend}
          disabled={!message.trim() || isLoading}
          className="bg-chat-red hover:bg-chat-red-dark text-white"
          size="sm"
        >
          {isLoading ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <>
              <span className="mr-1">Send</span>
              <SendIcon className="w-4 h-4" />
            </>
          )}
        </Button>
      </div>
    </div>
  );
};

export default ChatInput;