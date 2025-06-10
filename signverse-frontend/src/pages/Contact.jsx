const Contact = () => {
    return (
      <div className="max-w-lg mx-auto py-16 px-4 sm:px-6 lg:px-8 text-white">
        <h1 className="text-4xl font-bold text-cyan-400 mb-8">Contact Us</h1>
        <form className="space-y-6 bg-white/5 p-6 rounded-lg shadow-xl border border-white/10">
          <div>
            <label className="block text-sm font-medium text-cyan-200">Name</label>
            <input
              type="text"
              className="mt-1 w-full px-4 py-2 rounded-lg bg-white/10 border border-cyan-300 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              placeholder="Your Name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-cyan-200">Email</label>
            <input
              type="email"
              className="mt-1 w-full px-4 py-2 rounded-lg bg-white/10 border border-cyan-300 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-cyan-200">Message</label>
            <textarea
              rows={4}
              className="mt-1 w-full px-4 py-2 rounded-lg bg-white/10 border border-cyan-300 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              placeholder="Your message..."
            ></textarea>
          </div>
          <button
            type="submit"
            className="bg-cyan-600 hover:bg-cyan-700 text-white px-5 py-2 rounded-lg font-medium transition-all"
          >
            Send Message
          </button>
        </form>
      </div>
    );
  };
  
  export default Contact;
  