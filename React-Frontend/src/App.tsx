import { CreateProject } from "./pages/Projects/CreateProject";
import { UpdateProject } from "./pages/Projects/UpdateProject";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Signin from "./pages/Authentication/Signin";
import Signup from "./pages/Authentication/Signup";
import { Projects as Dashboard } from "./pages/Projects/ProjectsList";
import { CreateStory } from "./pages/Stories/CreateStories";
import UserProfile from "./pages/Users/UserProfile";
import { StoryProps } from "./pages/Stories/StoryProps";
import UpdateStories from "./pages/Stories/UpdateStories";

export const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/" element={<Signin />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/createProject" element={<CreateProject />} />
        <Route path="/updateProject/:projectId" element={<UpdateProject />} />
        <Route
          path="/updateStories/:projectId/:storyId"
          element={<UpdateStories />}
        />
        <Route path="/createStories/:projectId" element={<CreateStory />} />
        <Route path="/userProfile" element={<UserProfile />} />
        <Route path="/viewStories/:projectId" element={<StoryProps />} />
      </Routes>
    </Router>
  );
};
