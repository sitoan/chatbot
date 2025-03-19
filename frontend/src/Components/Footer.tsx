import React from "react";
import "../styles/Footer.css";

const Footer: React.FC = () => {
  return (
    <footer>
      <div className="container">
        <div className="sec aboutus">
          <h2>About Us</h2>
          <p>
            TourFlow is a modern and intelligent chatbot solution designed to
            optimize the user experience in searching for and booking tours.
          </p>
          <ul className="sci">
            <li>
              <a href="#">
                <i className="fa-brands fa-facebook-f"></i>
              </a>
            </li>
            <li>
              <a href="#">
                <i className="fa-brands fa-instagram"></i>
              </a>
            </li>
            <li>
              <a href="#">
                <i className="fa-brands fa-youtube"></i>
              </a>
            </li>
          </ul>
        </div>

        {/* Support Section */}
        <div className="sec quicklinks">
          <h2>Support</h2>
          <ul>
            <li>
              <a href="#">FAQ</a>
            </li>
            <li>
              <a href="#">Privacy Policy</a>
            </li>
            <li>
              <a href="#">Terms & Conditions</a>
            </li>
            <li>
              <a href="#">Help</a>
            </li>
            <li>
              <a href="#">Contact</a>
            </li>
          </ul>
        </div>

        {/* Tour Section */}
        <div className="sec quicklinks">
          <h2>Tour</h2>
          <ul>
            <li>
              <a href="#">Domestic Tours</a>
            </li>
            <li>
              <a href="#">International Tours</a>
            </li>
            <li>
              <a href="#">Special Offers</a>
            </li>
          </ul>
        </div>

        {/* Contact Us Section */}
        <div className="sec contact">
          <h2>Contact Us</h2>
          <ul className="info">
            <li>
              <span>
                <i className="fa-solid fa-phone"></i>
              </span>
              <p>
                <a href="tel:+84903043731">+84 903043731</a>
              </p>
            </li>
            <li>
              <span>
                <i className="fa-solid fa-envelope"></i>
              </span>
              <p>
                <a href="mailto:pmwangvinh@gmail.com">pmwangvinh@gmail.com</a>
              </p>
            </li>
          </ul>
        </div>
      </div>

      {/* Copyright Section */}
      <div className="copyrightText">
        <p>&copy; 2024 3tuitui. All Rights Reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
