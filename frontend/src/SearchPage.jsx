import { useState } from 'react'

export default function SearchPage({ onBack }) {
  const [keywords, setKeywords] = useState('')
  const [maxResults, setMaxResults] = useState(50)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState('')

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!keywords.trim()) return

    setLoading(true)
    setError('')
    setResults(null)

    try {
      const response = await fetch('http://localhost:8000/api/search-and-add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          keywords: keywords.trim(),
          max_results: parseInt(maxResults)
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Erreur lors de la recherche')
      }

      setResults(data)
      setKeywords('')
    } catch (err) {
      setError(err.message || 'Erreur de connexion avec le serveur')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(to bottom right, #0f172a, #1e293b, #0f172a)',
      padding: '32px 16px'
    }}>
      <div style={{
        maxWidth: '80rem',
        margin: '0 auto'
      }}>
        
        {/* Header avec bouton retour */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '48px'
        }}>
          <h1 style={{
            fontSize: '36px',
            fontWeight: 'bold',
            color: 'white',
            margin: 0
          }}>
            🔍 Rechercher des vidéos
          </h1>
          <button
            onClick={onBack}
            style={{
              padding: '8px 16px',
              backgroundColor: '#64748b',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '600',
              transition: 'background-color 0.2s'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = '#475569'}
            onMouseLeave={(e) => e.target.style.backgroundColor = '#64748b'}
          >
            ← Retour
          </button>
        </div>

        {/* Formulaire de recherche */}
        <div style={{
          backgroundColor: '#1e293b',
          padding: '32px',
          borderRadius: '12px',
          marginBottom: '32px',
          border: '1px solid #334155'
        }}>
          <form onSubmit={handleSearch}>
            <div style={{
              marginBottom: '24px'
            }}>
              <label style={{
                display: 'block',
                color: 'white',
                fontSize: '14px',
                fontWeight: '600',
                marginBottom: '8px'
              }}>
                Mots-clés de recherche
              </label>
              <input
                type="text"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="Ex: Cyphaka, RAP Gasy, Tsy Ho Bado..."
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  borderRadius: '8px',
                  color: 'white',
                  fontSize: '16px',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            <div style={{
              marginBottom: '24px'
            }}>
              <label style={{
                display: 'block',
                color: 'white',
                fontSize: '14px',
                fontWeight: '600',
                marginBottom: '8px'
              }}>
                Nombre maximum de résultats
              </label>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '16px'
              }}>
                <input
                  type="range"
                  min="1"
                  max="50"
                  value={maxResults}
                  onChange={(e) => setMaxResults(e.target.value)}
                  style={{
                    flex: 1,
                    cursor: 'pointer'
                  }}
                />
                <input
                  type="number"
                  min="1"
                  max="50"
                  value={maxResults}
                  onChange={(e) => setMaxResults(e.target.value)}
                  style={{
                    width: '80px',
                    padding: '8px 12px',
                    backgroundColor: '#0f172a',
                    border: '1px solid #334155',
                    borderRadius: '8px',
                    color: 'white',
                    fontSize: '14px'
                  }}
                />
              </div>
              <p style={{
                fontSize: '12px',
                color: '#94a3b8',
                margin: '8px 0 0 0'
              }}>
                Résultats: {maxResults}
              </p>
            </div>

            <button
              type="submit"
              disabled={loading || !keywords.trim()}
              style={{
                width: '100%',
                padding: '12px 16px',
                backgroundColor: loading ? '#dc2626' : '#ef4444',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontWeight: '600',
                fontSize: '16px',
                cursor: loading || !keywords.trim() ? 'not-allowed' : 'pointer',
                opacity: loading || !keywords.trim() ? 0.5 : 1,
                transition: 'background-color 0.2s'
              }}
              onMouseEnter={(e) => !loading && keywords.trim() && (e.target.style.backgroundColor = '#dc2626')}
              onMouseLeave={(e) => !loading && keywords.trim() && (e.target.style.backgroundColor = '#ef4444')}
            >
              {loading ? '⏳ Recherche en cours...' : '🔍 Rechercher et ajouter'}
            </button>
          </form>
        </div>

        {/* Message d'erreur */}
        {error && (
          <div style={{
            marginBottom: '24px',
            padding: '16px',
            backgroundColor: 'rgba(153, 27, 27, 0.3)',
            border: '1px solid #dc2626',
            borderRadius: '8px',
            color: '#fca5a5'
          }}>
            ❌ {error}
          </div>
        )}

        {/* Résultats */}
        {results && (
          <div style={{
            backgroundColor: '#1e293b',
            padding: '32px',
            borderRadius: '12px',
            border: '1px solid #334155'
          }}>
            <h2 style={{
              fontSize: '24px',
              fontWeight: '600',
              color: 'white',
              marginTop: 0,
              marginBottom: '24px'
            }}>
              📊 Résultats de la recherche
            </h2>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '16px',
              marginBottom: '24px'
            }}>
              <div style={{
                backgroundColor: '#0f172a',
                padding: '16px',
                borderRadius: '8px',
                borderLeft: '4px solid #10b981'
              }}>
                <p style={{ color: '#94a3b8', margin: '0 0 4px 0', fontSize: '12px' }}>Ajoutées</p>
                <p style={{ color: '#10b981', fontSize: '28px', fontWeight: 'bold', margin: 0 }}>
                  {results.added}
                </p>
              </div>

              <div style={{
                backgroundColor: '#0f172a',
                padding: '16px',
                borderRadius: '8px',
                borderLeft: '4px solid #f59e0b'
              }}>
                <p style={{ color: '#94a3b8', margin: '0 0 4px 0', fontSize: '12px' }}>Doublons</p>
                <p style={{ color: '#f59e0b', fontSize: '28px', fontWeight: 'bold', margin: 0 }}>
                  {results.skipped}
                </p>
              </div>

              <div style={{
                backgroundColor: '#0f172a',
                padding: '16px',
                borderRadius: '8px',
                borderLeft: '4px solid #ef4444'
              }}>
                <p style={{ color: '#94a3b8', margin: '0 0 4px 0', fontSize: '12px' }}>Erreurs</p>
                <p style={{ color: '#ef4444', fontSize: '28px', fontWeight: 'bold', margin: 0 }}>
                  {results.errors || 0}
                </p>
              </div>
            </div>

            {results.videos && results.videos.length > 0 && (
              <div>
                <h3 style={{
                  fontSize: '18px',
                  fontWeight: '600',
                  color: 'white',
                  marginTop: 0,
                  marginBottom: '16px'
                }}>
                  Vidéos ajoutées ({results.videos.length})
                </h3>
                <div style={{
                  maxHeight: '300px',
                  overflowY: 'auto',
                  borderRadius: '8px',
                  border: '1px solid #334155'
                }}>
                  {results.videos.map((video, idx) => (
                    <div
                      key={idx}
                      style={{
                        padding: '12px 16px',
                        borderBottom: idx < results.videos.length - 1 ? '1px solid #334155' : 'none',
                        color: '#e2e8f0',
                        fontSize: '14px'
                      }}
                    >
                      <p style={{ margin: 0, marginBottom: '4px', color: '#10b981' }}>
                        ✅ {video.title}
                      </p>
                      <p style={{ margin: 0, fontSize: '12px', color: '#94a3b8' }}>
                        {video.channel}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}