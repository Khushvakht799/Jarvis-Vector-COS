import { useState } from 'react';
import './App.css';

function App() {
  const [output, setOutput] = useState('');
  const [command, setCommand] = useState('chat');
  const [settingsVisible, setSettingsVisible] = useState(false);
  const [selectedField, setSelectedField] = useState('');
  const [use32kD, setUse32kD] = useState(false);

  // Обработчик кнопок полей
  const handleFieldClick = (field: string) => {
    setSelectedField(field);
    setOutput(`Вы выбрали поле: ${field}`);
  };

  // Обработчик выбора команды
  const handleCommandChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setCommand(e.target.value);
  };

  // Отправка команды на backend
  const handleSubmit = async () => {
    setOutput(`Jarvis выполняет команду "${command}" на поле "${selectedField}"...`);
    try {
      const response = await fetch('http://localhost:8000/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          command,
          field: selectedField,
          use32kD
        }),
      });
      const data = await response.json();
      setOutput(data.result || 'Результат пустой');
    } catch (err) {
      setOutput(`Ошибка соединения с сервером Jarvis: ${err}`);
    }
  };

  // Переключение меню настроек
  const toggleSettings = () => {
    setSettingsVisible(!settingsVisible);
  };

  // Переключение 32kD
  const toggle32kD = () => {
    setUse32kD(!use32kD);
  };

  return (
    <div className="App">
      <header>
        <h1>Jarvis GUI</h1>
      </header>

      <section className="fields">
        <button onClick={() => handleFieldClick('Поле 7Д')}>Поле 7Д</button>
        <button onClick={() => handleFieldClick('Поле 11Д')}>Поле 11Д</button>
        <button onClick={() => handleFieldClick('Поле 15Д')}>Поле 15Д</button>
        <button onClick={() => handleFieldClick('Поле 32кД')}>Поле 32кД</button>
      </section>

      <section className="commands">
        <label htmlFor="commandSelect">Команды:</label>
        <select id="commandSelect" value={command} onChange={handleCommandChange}>
          <option value="chat">Чат</option>
          <option value="db_update">Обновление БД</option>
          <option value="deploy">Deploy</option>
        </select>
        <button onClick={handleSubmit}>Отправить</button>
      </section>

      <section className="settings">
        <button onClick={toggleSettings}>Настройки</button>
        {settingsVisible && (
          <div className="settings-panel">
            <h3>Меню настроек GUI</h3>
            <label>
              <input type="checkbox" checked={use32kD} onChange={toggle32kD} />
              Использовать 32kD слой
            </label>
            {/* Добавляй дополнительные переключатели и настройки по необходимости */}
          </div>
        )}
      </section>

      <section className="output">
        <h3>Вывод:</h3>
        <div>{output}</div>
      </section>
    </div>
  );
}

export default App;
