import "../styles/PagesTourShow.css";
import { useStringContext } from "../ContextAPI/TourFlowProvider";

const PagesTourShow = () => {
  const { currentPage, setCurrentPage, totalPages } = useStringContext();

  const elements = [];

  const activeStyle = {
    color: "black",
    fontSize: "140%",
    fontWeight: "bold",
  };

  const defaultStyle = {};

  const renderPageNumber = (page: number) => (
    <li
      key={page}
      style={page === currentPage ? activeStyle : defaultStyle}
      onClick={() => setCurrentPage(page)}
    >
      {page}
    </li>
  );

  // Add the first few pages
  for (let i = 1; i <= 3 && i <= totalPages; i++) {
    elements.push(renderPageNumber(i));
  }

  // Add dots if currentPage > 5
  if (currentPage > 5) {
    elements.push(
      <li key="left-dots" style={defaultStyle}>
        ...
      </li>
    );
  }

  // Add the middle range (currentPage - 1, currentPage, currentPage + 1)
  const start = Math.max(4, currentPage - 1);
  const end = Math.min(totalPages - 2, currentPage + 1);

  for (let i = start; i <= end; i++) {
    elements.push(renderPageNumber(i));
  }

  // Add dots if currentPage < numsPage - 4
  if (currentPage < totalPages - 4) {
    elements.push(
      <li key="right-dots" style={defaultStyle}>
        ...
      </li>
    );
  }

  // Add the last few pages
  for (let i = Math.max(totalPages - 2, 4); i <= totalPages; i++) {
    elements.push(renderPageNumber(i));
  }

  return <ul id="pages">{elements}</ul>;
};

export default PagesTourShow;
