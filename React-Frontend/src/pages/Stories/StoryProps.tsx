import axios from "axios";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import StoryList from "./ViewStories";

interface Story {
  title: string;
  description: string;
  assignee: string;
  estimate: string;
  get_status_display: string;
  get_is_scheduled_display: string;
}

export const StoryProps = () => {
  const { projectId } = useParams();
  const [story, setStory] = useState<Array<Story>>([]);
  const [scheduledStories, setscheduledStories] = useState<Array<Story>>([]);
  const [unscheduledStories, setunscheduledStories] = useState<Array<Story>>(
    []
  );
  const [projectTitle, setProjectTitle] = useState("");
  const [pageChange, setPageChange] = useState(1);
  const [pageCount, setPageCount] = useState(1);

  let API_URL = `${
    process.env.REACT_APP_BASE_URL
  }/stories/?project_id=${projectId}&limit=2&offset=${(pageChange - 1) * 2}`;
  let API_PROJECT_URL = `${process.env.REACT_APP_BASE_URL}/projects/${projectId}/`;

  const fetchData = async (url: string) => {
    try {
      const response = await axios.get(url, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
      setStory([...response.data.results]);
      setPageCount(Math.ceil(response.data.count / 1));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`${process.env.REACT_APP_BASE_URL}/stories/${id}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
      fetchData(API_URL);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData(API_URL);
    const fetchProject = async (url: string) => {
      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        setProjectTitle(response.data.title);
      } catch (err) {
        console.error(err);
      }
    };
    fetchProject(API_PROJECT_URL);
  }, [projectId, pageChange]);

  useEffect(() => {
    const sortedStories = [...story].sort((a, b) => {
      if (a.status !== b.status) {
        return b.status - a.status;
      }

      return new Date(b.created_at) - new Date(a.created_at);
    });

    setscheduledStories(sortedStories.filter((s) => s.is_scheduled === 1));
    setunscheduledStories(sortedStories.filter((s) => s.is_scheduled === 2));
  }, [story]);

  return (
    <>
      <StoryList
        scheduledStories={scheduledStories}
        unscheduledStories={unscheduledStories}
        projectId={projectId}
        projectTitle={projectTitle}
        handleDelete={handleDelete}
        pageCount={pageCount}
        setPageChange={setPageChange}
      />
    </>
  );
};
