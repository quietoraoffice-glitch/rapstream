import { useState, useEffect } from 'react'
import SearchPage from './SearchPage'
import './App.css'

export default function App() {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [currentPage, setCurrentPage] = useState('home')

  useEffect(() => {
    fetchVideos()
  }, [])

  const fetchVideos = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await fetch('http://localhost:8000/api/videos')
      
      if (!response.ok) {
        throw new Error('Erreur lors de la récupération de la playlist')
      }

      const data = await response.json()
      setVideos(data.videos || [])

      if (data.videos && data.videos.length === 0) {
        setError('Votre playlist est vide')
      }
    } catch (err) {
      setError(err.message || 'Erreur de connexion avec le serveur')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {currentPage === 'search' ? (
        <SearchPage onBack={() => setCurrentPage('home')} />
      ) : (
        <div style={{
          minHeight: '100vh',
          background: 'linear-gradient(to bottom right, #0f172a, #1e293b, #0f172a)',
          padding: '32px 16px'
        }}>
          <div style={{
            maxWidth: '80rem',
            margin: '0 auto'
          }}>
            
            {/* Header */}
            <div style={{ textAlign: 'center', marginBottom: '48px' }}>
              <h1 style={{
                fontSize: '36px',
                fontWeight: 'bold',
                color: 'white',
                marginBottom: '8px'
              }}>
                🎤 RAP Gasy Streaming
              </h1>
              <p style={{
                color: '#cbd5e1',
                marginBottom: '24px'
              }}>Vidéos regroupées et organisées</p>
              
              {/* Boutons d'action */}
              <div style={{
                display: 'flex',
                gap: '12px',
                justifyContent: 'center',
                flexWrap: 'wrap'
              }}>
                <button
                  onClick={fetchVideos}
                  disabled={loading}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '8px 16px',
                    backgroundColor: loading ? '#dc2626' : '#ef4444',
                    color: 'white',
                    fontWeight: '600',
                    borderRadius: '8px',
                    border: 'none',
                    cursor: loading ? 'not-allowed' : 'pointer',
                    opacity: loading ? 0.5 : 1,
                    transition: 'background-color 0.2s'
                  }}
                  onMouseEnter={(e) => !loading && (e.target.style.backgroundColor = '#dc2626')}
                  onMouseLeave={(e) => !loading && (e.target.style.backgroundColor = '#ef4444')}
                >
                  {loading ? '⏳ Chargement...' : '🔄 Actualiser'}
                </button>

                <button
                  onClick={() => setCurrentPage('search')}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '8px 16px',
                    backgroundColor: '#3b82f6',
                    color: 'white',
                    fontWeight: '600',
                    borderRadius: '8px',
                    border: 'none',
                    cursor: 'pointer',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = '#2563eb'}
                  onMouseLeave={(e) => e.target.style.backgroundColor = '#3b82f6'}
                >
                  🔍 Rechercher
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div style={{
                marginBottom: '24px',
                padding: '16px',
                backgroundColor: 'rgba(153, 27, 27, 0.3)',
                border: '1px solid #dc2626',
                borderRadius: '8px',
                color: '#fca5a5'
              }}>
                {error}
              </div>
            )}

            {/* Loading State */}
            {loading && videos.length === 0 && (
              <div style={{
                textAlign: 'center',
                paddingTop: '48px',
                paddingBottom: '48px'
              }}>
                <p style={{ color: '#94a3b8' }}>Chargement de votre playlist...</p>
              </div>
            )}

            {/* Videos Grid */}
            {videos.length > 0 && (
              <div>
                <h2 style={{
                  fontSize: '20px',
                  fontWeight: '600',
                  color: 'white',
                  marginBottom: '24px'
                }}>
                  {videos.length} vidéo{videos.length > 1 ? 's' : ''}
                </h2>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                  gap: '20px'
                }}>
                  {videos.map((video, index) => (
                    <a
                      key={video.id}
                      href={video.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        position: 'relative',
                        backgroundColor: '#475569',
                        borderRadius: '8px',
                        overflow: 'hidden',
                        textDecoration: 'none',
                        display: 'flex',
                        flexDirection: 'column',
                        transition: 'transform 0.2s, box-shadow 0.2s',
                        cursor: 'pointer'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'scale(1.05)'
                        e.currentTarget.style.boxShadow = '0 0 30px rgba(239, 68, 68, 0.2)'
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)'
                        e.currentTarget.style.boxShadow = 'none'
                      }}
                    >
                      {/* Number Badge */}
                      <div style={{
                        position: 'absolute',
                        top: '8px',
                        left: '8px',
                        zIndex: 10,
                        backgroundColor: '#ef4444',
                        color: 'white',
                        borderRadius: '50%',
                        width: '32px',
                        height: '32px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '14px',
                        fontWeight: 'bold'
                      }}>
                        {index + 1}
                      </div>

                      {/* Thumbnail */}
                      <div style={{
                        position: 'relative',
                        overflow: 'hidden',
                        backgroundColor: '#334155',
                        aspectRatio: '16 / 9'
                      }}>
                        <img
                          src={video.thumbnail}
                          alt={video.title}
                          style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'cover',
                            transition: 'transform 0.2s'
                          }}
                          onMouseEnter={(e) => e.target.style.transform = 'scale(1.1)'}
                          onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
                        />
                        <div style={{
                          position: 'absolute',
                          inset: 0,
                          backgroundColor: 'rgba(0, 0, 0, 0.4)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '48px'
                        }}>
                          ▶️
                        </div>
                      </div>

                      {/* Title */}
                      <div style={{
                        padding: '16px',
                        flex: 1,
                        display: 'flex',
                        flexDirection: 'column'
                      }}>
                        <h3 style={{
                          fontSize: '14px',
                          fontWeight: '600',
                          color: 'white',
                          margin: 0,
                          display: '-webkit-box',
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: 'vertical',
                          overflow: 'hidden',
                          flex: 1,
                          transition: 'color 0.2s'
                        }}>
                          {video.title}
                        </h3>
                        <p style={{
                          fontSize: '12px',
                          color: '#94a3b8',
                          margin: '12px 0 0 0'
                        }}>Regarder sur YouTube →</p>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            )}

            {/* Empty State */}
            {!loading && videos.length === 0 && !error && (
              <div style={{
                textAlign: 'center',
                paddingTop: '48px',
                paddingBottom: '48px'
              }}>
                <p style={{ color: '#475569', fontSize: '18px' }}>Votre playlist est vide</p>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  )
}