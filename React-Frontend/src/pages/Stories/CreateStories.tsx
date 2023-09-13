import React, { useState, useEffect } from "react";
import "../Projects/ProjectForm.scss";
import { GenericDropdownList } from "../../components/Ui/Dropdown";
import Layout from "../../components/Layout";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

export const CreateStory = () => {
  const { projectId } = useParams();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [assignee, setAssignee] = useState(0);
  const [estimate, setEstimate] = useState(0);
  const [member, setMember] = useState<Array<number>>([]);
  const navigate = useNavigate();

  const handleUpdateSuccess = () => {
    navigate("/dashboard");
  };

  const API_URL = `${process.env.REACT_APP_BASE_URL}/projects/${projectId}/`;

  useEffect(() => {
    const fetchMembers = async (url: string) => {
      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        const memberArr = response.data.members;
        setMember(memberArr);
      } catch (err) {
        console.error(err);
      }
    };
    fetchMembers(API_URL);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BASE_URL}/stories/`,
        {
          title: title,
          description: description,
          assignee: assignee,
          estimate: estimate,
          project: projectId,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );
      handleUpdateSuccess();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Layout>
      <div className="main">
        <div className="header">
          <h1>CREATE STORY</h1>
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
                step="1"
                required
              />
            </div>
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
              Add Story
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
};
