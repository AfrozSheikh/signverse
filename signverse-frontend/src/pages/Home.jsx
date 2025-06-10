import LiveVideo from '../components/VideoStream';
import ASLChart from '../components/ASLChart';
import DetectedText from '../components/DetectedText';
import ControlButtons from '../components/Controls';

const Home = ({
  isVideoActive,
  startVideo,
  stopVideo,
  backendUrl,
  detectedText,
  statusMessage,
  handleClear,
  handleSpeak,
  isLoading,
}) => {
  return (
    <div className="py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      <div className="grid lg:grid-cols-2 gap-8">
        <LiveVideo
          isVideoActive={isVideoActive}
          startVideo={startVideo}
          stopVideo={stopVideo}
          backendUrl={backendUrl}
        />
        <ASLChart />
      </div>

      <DetectedText detectedText={detectedText} statusMessage={statusMessage} />

      <ControlButtons
        handleClear={handleClear}
        handleSpeak={handleSpeak}
        isLoading={isLoading}
        detectedText={detectedText}
      />
    </div>
  );
};

export default Home;
