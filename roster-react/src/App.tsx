
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import './App.css';

import Login from './components/Login';
import NotFound from './components/NotFound';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login/>}/>
        <Route path="*" element={<NotFound/>}/>
      </Routes>
    </Router>
  );
}

export default App;
