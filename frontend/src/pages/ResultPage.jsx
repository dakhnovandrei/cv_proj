import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import '../App.css';

const ResultPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Данные могут прийти сразу после анализа (location.state) или мы их загрузим из истории
  const [currentAnalysis, setCurrentAnalysis] = useState(location.state?.resultData || null);
  const [history, setHistory] = useState([]);

  
useEffect(() => {
  const fetchHistory = async () => {
    try {
      const res = await api.get('/api/v1/analysis_history?page=1&page_size=10');
      if (res.data?.history) setHistory(res.data.history);
    } catch (error) {
      console.error("Ошибка загрузки истории", error);
      if (error.response?.status === 401) navigate('/login');
    }
  };

  fetchHistory();
}, [navigate]);

  const handleHistoryClick = async (requestId) => {
      try {
          const res = await api.get(`/api/v1/analysis_history/${requestId}`);
          setCurrentAnalysis(res.data);
      } catch (error) {
          console.error(error);
      }
  };

  return (
    <div className="dash-layout">
      {/* Левая часть - Результат */}
      <div className="dash-main">
        {currentAnalysis ? (
            <>
                <h2 style={{marginBottom: '20px'}}>
                    Запрос от {new Date(currentAnalysis?.created_at || Date.now()).toLocaleString()}
                </h2>
                
                <div className="preview-box">
                    {/* Обрати внимание: image_url должен быть доступен браузеру. 
                        Если MinIO возвращает внутренний путь, нужно проксировать или использовать presigned url 
                        Для теста считаем, что URL валидный */}
                    <img src={currentAnalysis.image_url} alt="Analyzed Plant" onError={(e) => e.target.src = 'https://via.placeholder.com/300?text=Image+Not+Found'}/>
                </div>

                <div className="disease-info-card">
                    <h2>Информация про заболевание растения...</h2>
                    {currentAnalysis.results && currentAnalysis.results.length > 0 ? (
                        currentAnalysis.results.map((item, idx) => (
                            <div key={idx}>
                                <h3>{item.disease} (Уверенность: {Math.round(item.confidence * 100)}%)</h3>
                                <p><strong>Рекомендация:</strong> {item.recommendation}</p>
                            </div>
                        ))
                    ) : (
                        <p>Заболеваний не найдено или растение здорово.</p>
                    )}
                </div>
            </>
        ) : (
            <h2>Выберите анализ из истории справа</h2>
        )}

        <button className="btn btn-primary" style={{marginTop: '30px'}} onClick={() => navigate('/dashboard')}>
            Новый запрос
        </button>
      </div>

      {/* Правая часть - История */}
      <div className="dash-sidebar">
        <h3 style={{alignSelf: 'center'}}>Ваша история запросов</h3>
        
        <div className="history-list">
            {history.map((item) => (
                <div key={item.request_id} className="history-item" onClick={() => handleHistoryClick(item.request_id)}>
                    <div style={{fontWeight: 'bold', textAlign: 'center'}}>
                        {new Date(item.created_at).toLocaleDateString()}
                    </div>
                    {/* Можно добавить мини-превью или статус */}
                </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default ResultPage;