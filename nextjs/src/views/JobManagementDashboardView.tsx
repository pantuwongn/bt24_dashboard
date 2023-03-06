import { Layout } from "antd";
import { FC } from "react";
import DepartmentHierachyView from "./DepartmentHierarchyView";
import ProjectOverviewView from "./ProjectOverviewView";

const { Content, Sider } = Layout;

interface IProps {

}

const JobManagementDashboardView: FC<IProps> = ({ }: IProps) => {
  return (
    <Layout className="w-full h-full">
      <Sider width={300} style={{ paddingTop: 24, background: 'white' }}>
        <DepartmentHierachyView/>
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
            <ProjectOverviewView/>
          </Content>
        </Content>
      </Layout>
    </Layout>
  )
}

export default JobManagementDashboardView