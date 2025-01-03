import "../styles/AboutUs.css";
import NavigationBar from "./NavigationBar";
import Footer from "./Footer";
const AboutUs = () => {
  return (
    <>
      <NavigationBar />
      <div className="about-us-container">
        <div className="heading">
          <h1>About Us</h1>
          <p>
            TourFlow is a modern and intelligent chatbot solution designed to
            optimize the user experience when searching for and booking travel
            tours. It offers a seamless way for travelers to discover the best
            options based on their preferences and needs, making the booking
            process easier and more efficient.
          </p>
        </div>

        <div className="container">
          <section className="about"></section>
          <div className="about-image">
            {/* <img src="TourFlow_Img1.jpg" alt="TourFlow" /> */}
          </div>
          <div className="about-content">
            <h2>Who We Are</h2>
            <p>
              TourFlow is a modern and intelligent chatbot solution designed to
              optimize the user experience in searching for and booking travel
              tours. It aims to provide seamless assistance to travelers by
              helping them find the best tour options based on their preferences
              and needs.
            </p>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default AboutUs;
