import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import api from '../api/axios';
import '../App.css';
import plant1 from '../assets/plant1.jpg'

// Тебе понадобится изображение монстеры, положи его в папку public или src/assets
// import monsteraImg from '../assets/monstera.jpg'; 

const AuthPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const isRegister = location.pathname === '/register';

  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '' // Для регистрации
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isRegister) {
        if (formData.password !== formData.confirmPassword) {
            alert("Пароли не совпадают!");
            return;
        }
        // В users.py ожидает UserCreate (email, username, password)
        // Так как на макете username нет, используем email как username
        await api.post('/api/v1/reg', {
          email: formData.email,
          username: formData.username, 
          password: formData.password
        });
        alert("Регистрация успешна! Теперь войдите.");
        navigate('/login');
      } else {
        // Логин
        await api.post('/api/v1/login', {
          email: formData.email,
          password: formData.password
        });
        const cur_user = await api.get('/api/v1/profile');

        // Если успех, куки установлены, переходим в дешборд
        // Сохраним email в localStorage просто для отображения "Ваш никнейм"
        localStorage.setItem('username', cur_user.data.username);
        navigate('/dashboard');
      }
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Ошибка");
    }
  };

  return (
    <div className="split-screen">
      <div className="left-panel">
        <div className="auth-card">
          <h2 style={{color: '#8b5cf6', marginBottom: '10px'}}>
            {isRegister ? 'Регистрация' : 'Вход'}
          </h2>
          
          <form onSubmit={handleSubmit}>
            <label style={{display: 'block', textAlign: 'left', color: '#8d6e63'}}>Введите почту:</label>
            <input 
              className="auth-input" 
              name="email" 
              placeholder="example@mail.ru" 
              value={formData.email}
              onChange={handleChange}
              required
            />
            {isRegister &&(
              <>
                <label style={{display: 'block', textAlign: 'left', color: '#8d6e63'}}>Введите логин:</label>
                <input 
                  className="auth-input" 
                  name="username" 
                  placeholder="username" 
                  value={formData.username}
                  onChange={handleChange}
                  required
                />
              </>
            )}            
            <label style={{display: 'block', textAlign: 'left', color: '#8d6e63'}}>Введите пароль:</label>
            <input 
              className="auth-input" 
              name="password" 
              type="password" 
              placeholder="**********" 
              value={formData.password}
              onChange={handleChange}
              required
            />

            {isRegister && (
              <>
                <label style={{display: 'block', textAlign: 'left', color: '#8d6e63'}}>Подтвердите пароль:</label>
                <input 
                  className="auth-input" 
                  name="confirmPassword" 
                  type="password" 
                  placeholder="**********" 
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />
              </>
            )}
            

            <div style={{marginTop: '20px'}}>
              <button type="submit" className="btn btn-primary">
                {isRegister ? 'Зарегистрироваться' : 'Войти'}
              </button>
              
              {!isRegister && (
                 <button 
                   type="button" 
                   className="btn btn-primary"
                   onClick={() => navigate('/register')}
                 >
                   Регистрация
                 </button>
              )}
              {isRegister && (
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => navigate('/login')}
                >
                  Назад
                 </button>

              )}
            </div>
          </form>
        </div>
      </div>
      
      <div className="right-panel" style={{padding: 0}}>
         {/* Вставь сюда путь к своей картинке */}
         <img 
            src={plant1}
            alt="Plant" 
            className="plant-bg-image" 
         />
      </div>
    </div>
  );
};

export default AuthPage;