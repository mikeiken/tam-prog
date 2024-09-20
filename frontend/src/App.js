import './App.css';

function App() {
  return (
    <div className="App">
      <div className='intro'>
        <div className='video'>
          <video autoPlay muted loop className="background-video">
            <source src={process.env.PUBLIC_URL + '/background.mp4'} />
          </video>
        </div>
      </div>
    </div>
  );
}

export default App;