export const saveAccessToken = (accessToken) => {
  localStorage.setItem("access_token", accessToken);
};

export const getAccessToken = () => {
  return localStorage.getItem("access_token");
};

export const removeAccessToken = () => {
  localStorage.removeItem("access_token");
};
