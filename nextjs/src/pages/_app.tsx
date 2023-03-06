import type { AppProps } from 'next/app'

import '@ant-design/flowchart/dist/index.css'
import 'animate.css'
import '../styles/main.scss'
import '../styles/main.css'

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}

export default MyApp
