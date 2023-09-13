import React, { useState, useEffect } from "react";
import "../Projects/ProjectForm.scss";
import axios from "axios";
import { GenericDropdownList } from "../../components/Ui/Dropdown";
import { useNavigate, useParams } from "react-router-dom";
import Alert from "react-bootstrap/Alert";
import Layout from "../../components/Layout";

const UpdateStories = () => {
  const { projectId, storyId } = useParams();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [assignee, setAssignee] = useState(0);
  const [estimate, setEstimate] = useState(0);
  const [member, setMember] = useState<Array<number>>([]);
  const [statusId, setStatusId] = useState(1);
  const [scheduleId, setScheduleId] = useState(2);
  const [validationError, setValidationError] = useState("");
  const navigate = useNavigate();

  const handleUpdateSuccess = () => {
    navigate(`/viewStories/${projectId}`);
  };

  let statusChoices = {
    1: "Not Started",
    2: "Started",
    3: "Finished",
    4: "Delivered",
  };
  let scheduleStatus = { 1: "Scheduled", 2: "Not Scheduled" };

  const API_URL = `${process.env.REACT_APP_BASE_URL}/stories/${storyId}/`;
  let API_URL_MEMBERS = `${process.env.REACT_APP_BASE_URL}/projects/${projectId}/`;
  console.log(API_URL_MEMBERS);
  console.log(API_URL);

  useEffect(() => {
    const fetchData = async (url: string) => {
      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        setTitle(response.data.title);
        setDescription(response.data.description);
        setAssignee(response.data.assignee);
        setStatusId(response.data.status);
        setScheduleId(response.data.is_scheduled);
        setEstimate(response.data.estimate);
      } catch (err) {
        console.error(err);
      }
    };
    const fetchMembers = async (url: string) => {
      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        const memberArr = response.data.members;
        console.log(memberArr);
        setMember(memberArr);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData(API_URL);
    fetchMembers(API_URL_MEMBERS);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.patch(
        `${process.env.REACT_APP_BASE_URL}/stories/${storyId}/`,
        {
          title: title,
          description: description,
          assignee: assignee,
          estimate: estimate,
          status: statusId,
          is_scheduled: scheduleId,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );
      handleUpdateSuccess();
    } catch (error) {
      console.log(error.response.data);
      if (error.response && error.response.data) {
        const validationErrors = Object.values(error.response.data).join("\n");
        setValidationError(validationErrors);
      } else {
        console.error(error);
      }
    }
  };

  return (
    <Layout>
      <div className="main">
        {validationError && (
          <Alert variant="danger">
            <ul>
              {validationError.split("\n").map((error, index) => (
                <li key={index}>{error}</li>
              ))}
            </ul>
          </Alert>
        )}
        <div className="header">
          <h1>UPDATE STORY</h1>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="input-boxes">
            <div className="form-group">
              <input
                type="text"
                id="title"
                value={title}
                placeholder="Title"
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="text"
                id="description"
                value={description}
                placeholder="Description"
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="number"
                id="estimate"
                value={estimate}
                placeholder="Estimate (in hrs)"
                onChange={(e) => setEstimate(e.target.value)}
                min="0"
                step="0.5"
                required
              />
            </div>
          </div>

          <div className="checkbox">
            <GenericDropdownList
              items={Object.entries(statusChoices).map(([id, value]) => ({
                id,
                value,
              }))}
              selectedItem={statusId}
              setSelectedItem={setStatusId}
              label="Update Status"
            />
          </div>

          <div className="checkbox">
            <GenericDropdownList
              items={Object.entries(scheduleStatus).map(([id, value]) => ({
                id,
                value,
              }))}
              selectedItem={scheduleId}
              setSelectedItem={setScheduleId}
              label="Update Schedule"
            />
          </div>

          <div className="checkbox">
            <GenericDropdownList
              items={member.map((member) => ({
                id: member.id,
                value: member.first_name,
              }))}
              selectedItem={assignee}
              setSelectedItem={setAssignee}
              label="Assign a member"
            />
          </div>

          <div className="button">
            <button type="submit" onClick={handleSubmit}>
              Update Story
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default UpdateStories;
