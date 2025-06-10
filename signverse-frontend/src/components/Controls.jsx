const ControlButtons = ({ handleClear, handleSpeak, isLoading, detectedText }) => {
    return (
      <div className="flex flex-wrap gap-3 justify-center">
        <button
          onClick={handleClear}
          disabled={isLoading}
          className="px-5 py-2 bg-red-600 hover:bg-red-700 disabled:bg-red-800 disabled:opacity-50 text-white font-medium rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 flex items-center gap-2 text-sm"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {isLoading ? 'Clearing...' : 'Clear Text'}
        </button>
  
        <button
          onClick={handleSpeak}
          disabled={!detectedText.trim()}
          className="px-5 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:opacity-50 text-white font-medium rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 flex items-center gap-2 text-sm"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.617.815L5.75 14H2a1 1 0 01-1-1V7a1 1 0 011-1h3.75l2.633-2.815zm4.342-.186a1 1 0 011.414.014 6.75 6.75 0 010 9.543 1 1 0 11-1.428-1.4 4.75 4.75 0 000-6.743 1 1 0 01.014-1.414z" clipRule="evenodd" />
          </svg>
          Speak Text
        </button>
      </div>
    );
  };
  
  export default ControlButtons;
  