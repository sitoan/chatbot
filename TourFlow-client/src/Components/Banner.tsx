import React, { useEffect, useRef, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import "../styles/Banner.css";
const Banner: React.FC = () => {
  const bannerRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState<number>(0);

  const updateHeight = () => {
    if (bannerRef.current) {
      const width = bannerRef.current.offsetWidth;
      const calculatedHeight = width * 0.56;
      setHeight(calculatedHeight);
    }
  };

  useEffect(() => {
    updateHeight();
    window.addEventListener("resize", updateHeight);

    return () => {
      window.removeEventListener("resize", updateHeight);
    };
  }, []);

  return (
    <div
      ref={bannerRef}
      style={{
        display: "flex",
        width: "90%",
        height: `${height}px`,
        backgroundImage: `url("src/Imgs/BannerBackground.jpg")`,
        backgroundSize: "100% 100%",
        marginTop: 50,
        marginLeft: "auto",
        marginRight: "auto",
        borderRadius: 20,
      }}
    >
      <div id="banner-container">
        <div className="banner-item-1">
          <div className="sub-nav-item-1"></div>
          <div className="sub-nav-item-2">
            <div id="banner-titles">
              <p id="banner-subtitle">Elevate your travel</p>
              <p id="banner-title"> Experience The Magic of Travel !</p>
              <div id="banner-booktrip-button">Book trip now</div>
            </div>
          </div>
        </div>
        <div className="banner-item-2">
          <div id="knowmore-container">
            <h4>Know more</h4>
            <FontAwesomeIcon icon={faArrowRight} id="knowmore-icon" />
            <div id="knowmore-places">
              <div id="knowmore-places-images">
                <img
                  className="knowmore-image"
                  src="src/Imgs/knowmore-img2.jpg"
                  alt=""
                />
                <img
                  className="knowmore-image"
                  id="knowmore-image2"
                  src="src/Imgs/knowmore-img1.jpg"
                  alt=""
                />
                <img
                  className="knowmore-image"
                  id="knowmore-image3"
                  src="src/Imgs/knowmore-img3.jpg"
                  alt=""
                />
              </div>
              <div id="knowmore-places-titles">
                <h4>Awesome places</h4>
                <p>Discover the World One</p>
                <p>Adventure at A Time</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Banner;
