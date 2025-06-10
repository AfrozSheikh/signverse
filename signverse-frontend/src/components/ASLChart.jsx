const ASLChart = () => {
    return (
      <div className="bg-white/10 backdrop-blur-lg border border-white/15 p-5 rounded-xl shadow-lg border-2 border-cyan-400/30 transition-all hover:border-cyan-400/50">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-cyan-300">ASL Reference Chart</h3>
          <span className="text-sm bg-cyan-600/30 text-cyan-200 px-3 py-1 rounded-full">Guide</span>
        </div>
        <div className="h-80 bg-white/5 rounded-lg overflow-hidden border-2 border-white/10 flex items-center justify-center">
          <div className="text-center text-gray-400">
            <div className="text-4xl mb-2">🤟</div>
            <p className="text-sm">ASL Reference Chart</p>
            <p className="text-xs mt-1">A-Z Sign Language</p>
          </div>
        </div>
      </div>
    );
  };
  
  export default ASLChart;
  