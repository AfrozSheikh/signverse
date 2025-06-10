import React, { useRef, useEffect } from 'react';

const LiveVideo = ({ isVideoActive, startVideo, stopVideo, backendUrl }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    const videoElement = videoRef.current;
    if (videoElement && isVideoActive) {
      videoElement.src = `${backendUrl}/api/video_feed`;
    }
    return () => {
      if (videoElement) videoElement.src = '';
    };
  }, [isVideoActive]);

  return (
    <div className="bg-white/10 backdrop-blur-lg border border-white/15 p-5 rounded-xl shadow-lg border-2 border-cyan-400/30 transition-all hover:border-cyan-400/50">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-cyan-300">Live Sign Detection</h3>
        <span className={`text-sm px-3 py-1 rounded-full ${isVideoActive ? 'bg-green-600/30 text-green-200' : 'bg-yellow-600/30 text-yellow-200'}`}>
          {isVideoActive ? 'Active' : 'Ready'}
        </span>
      </div>
      <div className="h-80 bg-black/20 rounded-lg overflow-hidden border-2 border-white/10 relative">
        {isVideoActive ? (
          <img ref={videoRef} className="w-full h-full object-cover" alt="Sign language detection stream" />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50 text-gray-300">
            <div className="text-center">
              <div className="text-4xl mb-2">📹</div>
              <div className="text-sm">Camera ready</div>
              <button
                onClick={startVideo}
                className="mt-4 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white font-medium rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 text-sm"
              >
                Start Camera
              </button>
            </div>
          </div>
        )}
      </div>
      {isVideoActive && (
        <button
          onClick={stopVideo}
          className="mt-3 w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 text-sm"
        >
          Stop Camera
        </button>
      )}
    </div>
  );
};

export default LiveVideo;
