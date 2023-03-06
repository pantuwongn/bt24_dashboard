import Head from 'next/head'
import type { NextPage } from 'next'
import Container from '@/components/layout'
import JobManagementDashboardView from '@/views/JobManagementDashboardView'
import { useEffect } from 'react'
import { fetchOrganization } from '@/actions'

const Home: NextPage = () => {
  useEffect(() => {
    fetchOrganization()
  }, [])

  return (
    <>
      <div>
        <Head>
          <title>Bitrix24 Dashboard</title>
        </Head>
      </div>
      <Container
        title='Job Management Dashboard'
        className='m-0 p-0 mt-1'>
        <JobManagementDashboardView/>
      </Container>
    </>
  )
}

export default Home
