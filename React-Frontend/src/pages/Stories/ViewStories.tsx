import { useState } from "react";
import "./StoryList.scss";
import { Link } from "react-router-dom";
import Layout from "../../components/Layout";
import Pagination from "../../components/Pagination/Pagination";

interface Story {
  title: string;
  description: string;
  assignee: string;
  estimate: string;
  get_status_display: string;
  get_is_scheduled_display: string;
}
interface StoryListProps {
  scheduledStories: Story[];
  unscheduledStories: Story[];
  projectTitle: string;
  projectId: number;
}
const StoryList = ({
  scheduledStories,
  unscheduledStories,
  projectTitle,
  projectId,
  handleDelete,
  pageCount,
  setPageChange,
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const PageSize = 2;

  const statusChoices = {
    1: "Not Started",
    2: "Started",
    3: "Finished",
    4: "Delivered",
  };
  const scheduleChoices = {
    1: "Scheduled",
    2: "Not Scheduled",
  };
  return (
    <Layout>
      <div className="container mt-4">
        <div className="card">
          <div className="card-header">
            <h1 className="text-center">Story List</h1>
            <h4 className="text-center">{projectTitle}</h4>
          </div>
          <div className="card-body">
            <div className="d-flex">
              <div className="col">
                <h5 className="text-center">Scheduled Stories</h5>
                {scheduledStories.length > 0 ? (
                  scheduledStories.map((story) => (
                    <div className="card mb-3" key={story.id}>
                      <div className="card-body">
                        <h5 className="card-title">{story.title}</h5>
                        <p className="card-text">{story.description}</p>
                        <div className="d-flex justify-content-between align-items-center">
                          <span className="badge bg-secondary">
                            {story.name}
                          </span>
                          <span className="badge bg-info">
                            {story.estimate}Hrs.
                          </span>
                          <span className="badge bg-primary">
                            {statusChoices[story.status]}
                          </span>
                          <span className="badge bg-success">
                            {scheduleChoices[story.is_scheduled]}
                          </span>
                        </div>
                        <Link
                          to={`/updateStories/${projectId}/${story.id}`}
                          className="btn btn-primary mt-3"
                        >
                          Edit
                        </Link>
                        <button
                          className="btn btn-danger mt-3"
                          onClick={() => handleDelete(story.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-muted text-center">
                    No scheduled stories found.
                  </p>
                )}
              </div>

              <div className="col">
                <h5 className="text-center">Unscheduled Stories</h5>
                {unscheduledStories.length > 0 ? (
                  unscheduledStories.map((story) => (
                    <div className="card mb-3" key={story.id}>
                      <div className="card-body">
                        <h5 className="card-title">{story.title}</h5>
                        <p className="card-text">{story.description}</p>
                        <div className="d-flex justify-content-between align-items-center">
                          <span className="badge bg-secondary">
                            {story.name}
                          </span>
                          <span className="badge bg-info">
                            {story.estimate}Hrs.
                          </span>
                          <span className="badge bg-primary">
                            {statusChoices[story.status]}
                          </span>
                          <span className="badge bg-success">
                            {scheduleChoices[story.is_scheduled]}
                          </span>
                        </div>
                        <Link
                          to={`/updateStories/${projectId}/${story.id}`}
                          className="btn btn-primary mt-3"
                        >
                          Edit
                        </Link>
                        <button
                          className="btn btn-danger mt-3"
                          onClick={() => handleDelete(story.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-muted text-center">
                    No unscheduled stories found.
                  </p>
                )}
                <Pagination
                  className="pagination-bar"
                  currentPage={currentPage}
                  totalCount={pageCount}
                  pageSize={PageSize}
                  onPageChange={(page) => {
                    setPageChange(page);
                    setCurrentPage(page);
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default StoryList;
