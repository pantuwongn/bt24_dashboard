import { Layout } from "antd";
import { FC, useCallback, useEffect, useMemo } from "react";
import DepartmentHierachyView from "./DepartmentHierarchyView";
import ProjectOverviewView from "./ProjectOverviewView";
import { useLayoutStore, useOrganizationStore } from "@/store";
import { fetchTaskByDepartmentId } from "@/actions";

const { Content, Sider } = Layout;

interface IProps {
}

const JobManagementDashboardView: FC<IProps> = ({ }: IProps) => {
  const {
    selectedDepartmentId,
    currentDepartmentProject
  } = useOrganizationStore()
  const {
    setIsLoading
  } = useLayoutStore()

  const doFetchTaskByDepartmentId = useCallback(async () => {
    if (selectedDepartmentId !== null) {
      setIsLoading(true)
      await fetchTaskByDepartmentId(selectedDepartmentId)
      setIsLoading(false)
    }
  }, [selectedDepartmentId, setIsLoading])
  useEffect(() => {
    doFetchTaskByDepartmentId()
  }, [doFetchTaskByDepartmentId])

  const departmentProject = currentDepartmentProject()

  return (
    <Layout className="w-full h-full">
      <Sider width={300} style={{ paddingTop: 24, background: 'white' }}>
        <DepartmentHierachyView />
      </Sider>

      <Layout style={{ padding: 24 }}>
        <Content
          style={{
            margin: 0,
            minHeight: 280
          }}
        >
          <Content
            style={{
              padding: 24,
              background: 'white'
            }}>
            {departmentProject === null ?
              <div className="font-bold text-3xl text-center">Please select any department</div> :
              <ProjectOverviewView departmentProject={departmentProject}/>
            }
          </Content>
        </Content>
      </Layout>
    </Layout>
  )
}

export default JobManagementDashboardView