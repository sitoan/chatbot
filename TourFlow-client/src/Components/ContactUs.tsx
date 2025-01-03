import "../styles/ContactUs.css"; // Import the CSS
import NavigationBar from "./NavigationBar";
import Footer from "./Footer";

// Contacts Infos Component (Updated class name)
const ContactInfos = () => {
  return (
    <div className="contacts infos">
      <h3>Contact Info</h3>
      <div className="infoBox">
        <div>
          <span>
            <i className="fa-solid fa-location-dot"></i>
          </span>
          <p>Ni Su Huynh Lien, Tan Binh, Ho Chi Minh City</p>
        </div>
        <div>
          <span>
            <i className="fa-solid fa-envelope"></i>
          </span>
          <a href="mailto:tourflowdev@gmail.com">tourflowdev@gmail.com</a>
        </div>
        <div>
          <span>
            <i className="fa-solid fa-phone"></i>
          </span>
          <a href="tel:+84903043731">+84 903043731</a>
        </div>
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
    </div>
  );
};

const ContactMap = () => {
  return (
    <div className="contacts map">
      <iframe
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d62705.67372884592!2d106.61205907124204!3d10.803299584161023!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3175293818af3a73%3A0xcd8d16d1180acc8b!2zVMOibiBCw6xuaCwgSOG7kyBDaMOtIE1pbmgsIFZp4buHdCBOYW0!5e0!3m2!1svi!2s!4v1731846305548!5m2!1svi!2s"
        style={{ border: 0 }}
        allowFullScreen
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
      ></iframe>
    </div>
  );
};

// Main Component
const ContactUs = () => {
  return (
    <div>
      <NavigationBar />
      <div className="contactsUs">
        <h4>Get in Touch</h4>
        <div className="box">
          <ContactInfos /> {/* Updated component name */}
          <ContactMap />
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ContactUs;
