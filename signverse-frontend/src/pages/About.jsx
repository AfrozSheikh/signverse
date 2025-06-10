const About = () => {
    return (
      <div className="max-w-3xl mx-auto py-16 px-4 sm:px-6 lg:px-8 text-white space-y-6">
        <h1 className="text-4xl font-bold text-cyan-400">About SignVerse</h1>
        <p className="text-lg leading-relaxed text-gray-300">
          <strong>SignVerse</strong> is an innovative sign language interpretation platform that translates real-time American Sign Language (ASL) gestures into readable text and speech using computer vision and machine learning.
        </p>
        <p className="text-lg leading-relaxed text-gray-300">
          This tool empowers communication for the deaf and hard of hearing, enabling a more inclusive and accessible digital experience. Built using <strong>React.js</strong> and <strong>Flask</strong>, SignVerse utilizes <strong>MediaPipe</strong> for hand tracking and a trained <strong>Random Forest model</strong> for prediction.
        </p>
        <p className="text-sm text-gray-500 mt-6">Version 1.0 – Built with ❤️ by Team SignVerse</p>
      </div>
    );
  };
  
  export default About;
  