const DetectedText = ({ detectedText, statusMessage }) => {
    return (
      <div className="max-w-2xl mx-auto mb-6">
        <h3 className="text-base font-medium text-cyan-300 mb-1 text-center">Detected Text</h3>
        <div className="bg-white/10 backdrop-blur-lg border border-white/10 p-3 min-h-16 rounded-lg text-base text-white shadow-inner flex items-center justify-center">
          {detectedText ? (
            <span className="text-white animate-pulse font-mono text-lg tracking-wider">
              {detectedText}
            </span>
          ) : (
            <span className="text-gray-400 text-sm">{statusMessage}</span>
          )}
        </div>
      </div>
    );
  };
  
  export default DetectedText;
  