import type { NextPage } from "next";
import Head from "next/head";
import LoginView from "@/views/LoginView";

const LoginPage: NextPage = () => {

  return (
    <>
      <div>
        <Head>
          <title>Bitrix24 Dashboard Login</title>
        </Head>
      </div>

      <div className="w-full h-screen flex flex-col items-center justify-center">
        <LoginView/>
      </div>
    </>
  )
}

export default LoginPage