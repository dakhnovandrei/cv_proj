import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import '../App.css';
import example1 from '../assets/example1.jpg'

const Dashboard = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  
  // Получаем email из localStorage или ставим заглушку
  const userName = localStorage.getItem('username') || "Ваш никнейм";

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
        alert("Сначала загрузите фото");
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Отправляем на анализ
      const response = await api.post('/api/v2/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      // Переходим на страницу результатов
      navigate('/result', { state: { resultData: response.data } });
    } catch (error) {
      console.error(error);
      if (error.response?.status === 401) {
          alert("Сессия истекла");
          navigate('/login');
      } else {
          // Для демо-режима заглушки это не должно сработать, но на всякий случай
          alert("Ошибка анализа: " + (error.response?.data?.detail || "Unknown error"));
      }
    }
  };

  return (
    <div className="dash-layout">
      {/* Левая часть - Загрузка */}
      <div className="dash-main">
        {/* ИСПРАВЛЕНИЕ: Убрали alignSelf, теперь заголовок по центру над фото */}
        <h2 style={{ marginBottom: '15px' }}>Пример фото</h2>
        
        {/* ИСПРАВЛЕНИЕ: Увеличили размер контейнера фото (300x200 вместо 150x100) */}
        <div style={{
            width: '300px', 
            height: '200px', 
            marginBottom: '30px', 
            overflow: 'hidden', 
            borderRadius: '10px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        }}>
            <img 
                src={example1}
                alt="example" 
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                onError={(e) => e.target.src = 'https://via.placeholder.com/300x200?text=Пример+растения'}
            />
        </div>

        {/* Область превью загружаемого фото */}
        <div className="preview-box" onClick={() => fileInputRef.current.click()} style={{cursor: 'pointer'}}>
          {preview ? (
            <img src={preview} alt="Upload preview" />
          ) : (
            <div className="preview-text">Ваше фото...</div>
          )}
        </div>
        
        <input 
            type="file" 
            ref={fileInputRef} 
            style={{display: 'none'}} 
            onChange={handleFileSelect}
            accept="image/*"
        />

        <div style={{display: 'flex', gap: '20px'}}>
            <button className="btn btn-primary" onClick={() => fileInputRef.current.click()}>
                Загрузить фото
            </button>
            <button className="btn btn-primary" onClick={handleAnalyze}>
                Анализировать
            </button>
        </div>
      </div>

      {/* Правая часть - Инструкция и профиль */}
      <div className="dash-sidebar">
        <div style={{alignSelf: 'center', textAlign: 'center', marginBottom: '40px'}}>
            <h3>{userName}</h3>
            <button className="btn" style={{background: '#bcebc3', color: '#1f2937'}} onClick={() => navigate('/result')}>
                История
            </button>
        </div>

        <h1>Инструкция:</h1>
        <ol style={{fontSize: '1.2em', lineHeight: '1.6'}}>
            <li>Загрузите ваше фото. Старайтесь чтобы проблемная часть вашего растения была хорошо видна.</li>
            <li>Нажмите кнопку Анализировать.</li>
            <li>После этого вам предоставится предполагаемое заболевание растения.</li>
        </ol>
      </div>
    </div>
  );
};

export default Dashboard;