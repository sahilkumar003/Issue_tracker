import Header from "./navigation/Header";
import Footer from "./navigation/Footer";

export default function Layout(props) {
  return (
    <div>
      <Header />
      {props.children}
      <Footer />
    </div>
  );
}
