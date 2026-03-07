import Header from "./Header";

const Layout = ({ children }) => {
  return (
    <>
      <Header />
      <main className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
        {children}
      </main>
    </>
  );
};

export default Layout;
