import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {Auth0Provider} from '@auth0/auth0-react'
import './index.css'
import App from './App.jsx'
import {domainId, clientId} from './env.js'

const root = createRoot(document.getElementById('root'))

root.render(
  <Auth0Provider
    domain={{domainId}}
    clientId={{clientId}}
    authorizationParams={{
      redirect_uri: window.location.origin,
      audience: "this-is-my-super-awesome-project-api",
      scope: "defined token capabilities"
    }}
  >
    <App />
  </Auth0Provider>
)
