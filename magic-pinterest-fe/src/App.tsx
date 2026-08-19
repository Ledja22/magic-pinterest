import { useState } from 'react'

import './App.css'
import { FileUploadDropZone} from "./components/application/file-upload/file-upload-base.tsx";

function App() {
  const [count] = useState(0)

  return (
   <FileUploadDropZone key={count}></FileUploadDropZone>
  )
}

export default App
