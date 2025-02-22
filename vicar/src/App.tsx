import './App.css'
import { RouterProvider } from 'react-router-dom'
import { router } from './routes'
export const App =() => {
  // const [count, setCount] = useState(0)

  return <RouterProvider router={router} />
}

export default App
