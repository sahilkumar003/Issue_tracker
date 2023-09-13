import { Link } from "react-router-dom";

const Header = () => {
  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-md-12 px-0">
          <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <Link to="/dashboard" className="navbar-brand">
              &nbsp; Issue Tracker System
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-toggle="collapse"
              data-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ml-auto">
                <li className="nav-item">
                  <Link to="/dashboard" className="nav-link">
                    Dashboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/createProject" className="nav-link">
                    Create Project
                  </Link>
                </li>
                <li className="nav-item" id="profileIcon">
                  <Link to="/userProfile" className="nav-link">
                    Profile
                  </Link>
                </li>
              </ul>
            </div>
          </nav>
        </div>
      </div>
    </div>
  );
};

export default Header;
