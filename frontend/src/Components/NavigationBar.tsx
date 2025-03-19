import { useEffect, useState } from "react";
import "../styles/NavigationBar.css";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import ModalBookTour from "./ModalBookTour";

const NavigationBar = () => {
  const [isOpen, setIsOpen] = useState(false); // Trạng thái menu (hamburger)
  const [isNavVisible, setIsNavVisible] = useState(true); // Trạng thái của nav-bar
  const [isModalOpen, setModalOpen] = useState(false);
  const handleOpenModal = () => setModalOpen(true);
  const handleCloseModal = () => setModalOpen(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 890) {
        setIsNavVisible(true);
        setIsOpen(false);
      } else {
        setIsNavVisible(false);
      }
    };

    window.addEventListener("resize", handleResize);

    handleResize();
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <div className="nav-bar">
      {isNavVisible && (
        <Link to="/" className="flex-item item-1">
          <div>
            {/* <img id="logo-nav-bar" src="src/Imgs/companyLogo.png" alt="" /> */}
            <img
              id="logo-nav-bar"
              src="https://cdn.glitch.global/b0b642c1-36db-486f-b55f-b05d4498b10c/companyLogo.png?v=1732192832130"
              alt=""
            />
          </div>
        </Link>
      )}

      {/* Menu */}
      <div className={`flex-item item-2 ${isOpen ? "active" : "noactive"}`}>
        <Link to="/" className="custom-link">
          <div className="nav-item">Home</div>
        </Link>
        <Link to="/about_us" className="custom-link">
          <div className="nav-item">About</div>
        </Link>
        <Link to="/contact_us" className="custom-link">
          <div className="nav-item">Contact</div>
        </Link>
        {sessionStorage.getItem("isAdmin") && (
          <Link to="/post_tour" className="custom-link">
            <div className="nav-item">Tour</div>
          </Link>
        )}
      </div>

      {/* Nav login section */}
      <div className="flex-item item-3">
        {sessionStorage.getItem("jwt") ? (
          <Link to={`/profile`} className="custom-link">
            <div
              id="nav-login"
              onClick={() => {
                console.log("logedin");
              }}
            >
              <img
                src={
                  sessionStorage.getItem("avaUrl") ||
                  "https://static.vecteezy.com/system/resources/thumbnails/005/129/844/small/profile-user-icon-isolated-on-white-background-eps10-free-vector.jpg"
                }
              />
              <h6>{sessionStorage.getItem("name")}</h6>
            </div>
          </Link>
        ) : (
          <div
            id="nav-login"
            onClick={() => {
              handleOpenModal();
              console.log("log in");
            }}
          >
            <FontAwesomeIcon icon={faUser} id="user_icon" />
            <h6>Login</h6>
          </div>
        )}
      </div>

      {/* Hamburger icon for small screens */}
      <div id="nav-bar-toggle" onClick={toggleMenu}>
        ☰
      </div>

      <ModalBookTour
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      ></ModalBookTour>
    </div>
  );
};

export default NavigationBar;
