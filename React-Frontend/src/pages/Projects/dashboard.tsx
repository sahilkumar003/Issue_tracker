import "./Projects.scss";
import "../../components/navigation/Footer.scss";
import { Link } from "react-router-dom";

export function ProjectView({ project }) {
  return (
    <div className="main-container">
      <div className="row">
        <div className="card mb-3">
          <div className="card-body">
            <h5 className="card-title d-flex justify-content-between">
              {project.title}
              <div className="btn-group">
                <div>
                  <Link
                    to={`/updateProject/${project.id}`}
                    className="btn btn-primary"
                    id="editBtn"
                  >
                    Edit
                  </Link>
                </div>
              </div>
            </h5>
            <p className="card-text">{project.description}</p>
            <div className="btn-group">
              <Link
                to={`/createStories/${project.id}`}
                className="btn btn-primary"
                id="createStoryBtn"
              >
                Create Stories
              </Link>
              <Link
                to={`/viewStories/${project.id}`}
                className="btn btn-secondary"
                id="editStoryBtn"
              >
                View Stories
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
