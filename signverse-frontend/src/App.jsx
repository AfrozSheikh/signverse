
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
// import NotFound from './pages/NotFound';

function App() {
  const [isVideoActive, setIsVideoActive] = useState(false);
  const [detectedText, setDetectedText] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const backendUrl = 'http://localhost:5000'; // Update if needed

  const startVideo = () => {
    setIsVideoActive(true);
  };

  const stopVideo = () => {
    setIsVideoActive(false);
  };

  const handleClear = async () => {
    try {
      const res = await fetch(`${backendUrl}/api/clear`);
      const data = await res.json();
      setDetectedText('');
      setStatusMessage(data.message);
    } catch (error) {
      console.error('Error clearing text:', error);
    }
  };

  const handleSpeak = async () => {
    try {
      setIsLoading(true);
      const res = await fetch(`${backendUrl}/api/speak`);
      const data = await res.json();
      setStatusMessage(data.message);
    } catch (error) {
      console.error('Error during text-to-speech:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-black text-white">
        <Navbar />
        <Routes>
          <Route
            path="/"
            element={
              <Home
                isVideoActive={isVideoActive}
                startVideo={startVideo}
                stopVideo={stopVideo}
                backendUrl={backendUrl}
                detectedText={detectedText}
                statusMessage={statusMessage}
                handleClear={handleClear}
                handleSpeak={handleSpeak}
                isLoading={isLoading}
              />
            }
          />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          {/* <Route path="*" element={<NotFound />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;


// import React, { useState, useEffect, useRef } from 'react';

// const App = () => {
//   const [detectedText, setDetectedText] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [statusMessage, setStatusMessage] = useState('Signs will appear here...');
//   const [isVideoActive, setIsVideoActive] = useState(false);
//   const videoRef = useRef(null);
//   const backendUrl = 'http://127.0.0.1:5000'; // Update if your backend is hosted elsewhere

//   // Fetch detected text from backend
//   useEffect(() => {
//     const fetchDetectedText = async () => {
//       try {
//         const response = await fetch(`${backendUrl}/api/get_output`);
//         const data = await response.json();
        
//         if (data.text && data.text.trim() !== '') {
//           setDetectedText(data.text);
//           setStatusMessage('');
//         } else if (detectedText === '') {
//           setStatusMessage('Signs will appear here...');
//         }
//       } catch (error) {
//         console.error('Error fetching detected text:', error);
//         setStatusMessage('Connection error...');
//       }
//     };

//     const interval = setInterval(fetchDetectedText, 500);
//     return () => clearInterval(interval);
//   }, [detectedText]);

//   // Handle video feed
//   useEffect(() => {
//     const videoElement = videoRef.current;
//     if (videoElement && isVideoActive) {
//       videoElement.src = `${backendUrl}/api/video_feed`;
//     }

//     return () => {
//       // Clean up when component unmounts or video is stopped
//       if (videoElement) {
//         videoElement.src = '';
//       }
//     };
//   }, [isVideoActive]);

//   // Start video feed
//   const startVideo = () => {
//     setIsVideoActive(true);
//     setStatusMessage('Initializing camera...');
//   };

//   // Stop video feed
//   const stopVideo = async () => {
//     try {
//       await fetch(`${backendUrl}/api/stop`, {
//         method: 'POST',
//       });
//       setIsVideoActive(false);
//     } catch (error) {
//       console.error('Error stopping video:', error);
//     }
//   };

//   // Clear detected text
//   const handleClear = async () => {
//     setIsLoading(true);
//     try {
//       const response = await fetch(`${backendUrl}/api/clear`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' }
//       });
      
//       const data = await response.json();
//       if (data.success) {
//         setDetectedText('');
//         setStatusMessage('Text cleared successfully');
//         setTimeout(() => {
//           setStatusMessage('Signs will appear here...');
//         }, 1500);
//       }
//     } catch (error) {
//       console.error('Error clearing text:', error);
//       setStatusMessage('Error clearing text');
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // Speak detected text
//   const handleSpeak = async () => {
//     if (!detectedText.trim()) return;
    
//     try {
//       await fetch(`${backendUrl}/api/speak`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' }
//       });
//     } catch (error) {
//       console.error('Error speaking text:', error);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 text-gray-100 font-sans flex flex-col">
//       {/* Navbar */}
//       <nav className="w-full px-4 sm:px-6 py-4 flex justify-between items-center bg-slate-800/80 backdrop-blur-md fixed top-0 left-0 z-50 shadow-lg">
//         <h1 className="text-3xl sm:text-4xl font-bold text-cyan-400">SignVerse</h1>
//         <ul className="flex gap-4 sm:gap-8 text-lg sm:text-xl font-medium">
//           <li><a href="/" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">Home</a></li>
//           <li><a href="/about" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">About</a></li>
//           <li><a href="/how-it-works" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">How It Works</a></li>
//           <li><a href="/practice" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">Practice</a></li>
//           <li><a href="/contact" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">Contact</a></li>
//         </ul>
//       </nav>
      
//       {/* Main Content */}
//       <main className="pt-24 px-4 pb-8 flex-1 w-full max-w-4xl mx-auto">
//         <div className="text-center mb-6">
//           <h2 className="text-2xl sm:text-3xl font-bold text-cyan-400 mb-2">
//             Real-Time Sign Language Detection
//           </h2>
//           <p className="text-gray-300 max-w-xl mx-auto text-sm">
//             Communicate seamlessly with our AI-powered sign language detection system
//           </p>
//         </div>

//         <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
//           {/* ASL Chart */}
//           <div className="bg-white/10 backdrop-blur-lg border border-white/15 p-5 rounded-xl shadow-lg border-2 border-cyan-400/30 transition-all hover:border-cyan-400/50">
//             <div className="flex items-center justify-between mb-4">
//               <h3 className="text-xl font-semibold text-cyan-300">ASL Reference Chart</h3>
//               <span className="text-sm bg-cyan-600/30 text-cyan-200 px-3 py-1 rounded-full">Guide</span>
//             </div>
//             <div className="h-80 bg-white/5 rounded-lg overflow-hidden border-2 border-white/10 flex items-center justify-center">
//               <div className="text-center text-gray-400">
//                 <div className="text-4xl mb-2">🤟</div>
//                 <p className="text-sm">ASL Reference Chart</p>
//                 <p className="text-xs mt-1">A-Z Sign Language</p>
//               </div>
//             </div>
//           </div>
        
//           {/* Live Video */}
//           <div className="bg-white/10 backdrop-blur-lg border border-white/15 p-5 rounded-xl shadow-lg border-2 border-cyan-400/30 transition-all hover:border-cyan-400/50">
//             <div className="flex items-center justify-between mb-4">
//               <h3 className="text-xl font-semibold text-cyan-300">Live Sign Detection</h3>
//               <span className={`text-sm px-3 py-1 rounded-full ${isVideoActive ? 'bg-green-600/30 text-green-200' : 'bg-yellow-600/30 text-yellow-200'}`}>
//                 {isVideoActive ? 'Active' : 'Ready'}
//               </span>
//             </div>
//             <div className="h-80 bg-black/20 rounded-lg overflow-hidden border-2 border-white/10 relative">
//               {isVideoActive ? (
//                 <img 
//                   ref={videoRef}
//                   className="w-full h-full object-cover" 
//                   alt="Sign language detection stream"
//                 />
//               ) : (
//                 <div className="absolute inset-0 flex items-center justify-center bg-black/50 text-gray-300">
//                   <div className="text-center">
//                     <div className="text-4xl mb-2">📹</div>
//                     <div className="text-sm">Camera ready</div>
//                     <button 
//                       onClick={startVideo}
//                       className="mt-4 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white font-medium rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 text-sm"
//                     >
//                       Start Camera
//                     </button>
//                   </div>
//                 </div>
//               )}
//             </div>
//             {isVideoActive && (
//               <button 
//                 onClick={stopVideo}
//                 className="mt-3 w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 text-sm"
//               >
//                 Stop Camera
//               </button>
//             )}
//           </div>
//         </div>

//         {/* Detected Text */}
//         <div className="max-w-2xl mx-auto mb-6">
//           <h3 className="text-base font-medium text-cyan-300 mb-1 text-center">Detected Text</h3>
//           <div className="bg-white/10 backdrop-blur-lg border border-white/10 p-3 min-h-16 rounded-lg text-base text-white shadow-inner flex items-center justify-center">
//             {detectedText ? (
//               <span className="text-white animate-pulse font-mono text-lg tracking-wider">
//                 {detectedText}
//               </span>
//             ) : (
//               <span className="text-gray-400 text-sm">{statusMessage}</span>
//             )}
//           </div>
//         </div>

//         {/* Controls */}
//         <div className="flex flex-wrap gap-3 justify-center">
//           <button 
//             onClick={handleClear}
//             disabled={isLoading}
//             className="px-5 py-2 bg-red-600 hover:bg-red-700 disabled:bg-red-800 disabled:opacity-50 text-white font-medium rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 flex items-center gap-2 text-sm"
//           >
//             <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
//               <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
//             </svg>
//             {isLoading ? 'Clearing...' : 'Clear Text'}
//           </button>

//           <button 
//             onClick={handleSpeak}
//             disabled={!detectedText.trim()}
//             className="px-5 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:opacity-50 text-white font-medium rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 flex items-center gap-2 text-sm"
//           >
//             <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
//               <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.617.815L5.75 14H2a1 1 0 01-1-1V7a1 1 0 011-1h3.75l2.633-2.815zm4.342-.186a1 1 0 011.414.014 6.75 6.75 0 010 9.543 1 1 0 11-1.428-1.4 4.75 4.75 0 000-6.743 1 1 0 01.014-1.414z" clipRule="evenodd" />
//             </svg>
//             Speak Text
//           </button>
//         </div>
//       </main>

//       {/* Footer */}
//       <footer className="text-center py-4 text-xs sm:text-sm text-gray-400 border-t border-gray-800 mt-6">
//         <div className="container mx-auto px-4">
//           <p>&copy; 2025 SignVerse. All rights reserved.</p>
//           <p className="mt-1">Bridging communication gaps through AI technology</p>
//         </div>
//       </footer>
//     </div>
//   );
// };

// export default App;