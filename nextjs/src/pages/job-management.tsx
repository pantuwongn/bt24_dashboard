import Head from 'next/head'
import type { NextPage } from 'next'
import Container from '@/components/layout'
import JobManagementDashboardView from '@/views/JobManagementDashboardView'
import { useEffect } from 'react'
import { fetchOrganization } from '@/actions'
import { useRouter } from 'next/router'
import { useOrganizationStore } from '@/store'

const Home: NextPage = () => {
  const router = useRouter()
  const { setSelectedDepartmentId } = useOrganizationStore()

  useEffect(() => {
    fetchOrganization()
  }, [])

  useEffect(() => {
    if (router.query.departmentId) {
      setSelectedDepartmentId(router.query.departmentId as string)
    }
  }, [router, setSelectedDepartmentId])

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
