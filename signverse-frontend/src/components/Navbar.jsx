// src/components/Navbar.jsx
import React from 'react';

const Navbar = () => {
  return (
    <nav className="w-full px-4 sm:px-6 py-4 flex justify-between items-center bg-slate-800/80 backdrop-blur-md fixed top-0 left-0 z-50 shadow-lg">
      <h1 className="text-3xl sm:text-4xl font-bold text-cyan-400">SignVerse</h1>
      <ul className="flex gap-4 sm:gap-8 text-lg sm:text-xl font-medium">
        <li><a href="/" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">Home</a></li>
        <li><a href="/about" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">About</a></li>
        <li><a href="/how-it-works" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">How It Works</a></li>
        <li><a href="/practice" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">Practice</a></li>
        <li><a href="/contact" className="hover:text-cyan-400 transition-colors px-3 py-2 rounded-lg">Contact</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;
