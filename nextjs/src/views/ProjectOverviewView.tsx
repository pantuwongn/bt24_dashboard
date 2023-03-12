import ProjectBudgetColumnChart from "@/components/chart/column/project-budget-column";
import ProjectStatusPieChart from "@/components/chart/pie/project-status-pie";
import { Card } from "antd";
import { FC } from "react";
import ProjectTimeStatusView from "./ProjectTimeStatusView";
import ProjectFocusAndWorkloadView from "./ProjectFocusAndWorkloadView";
import IncomingProjectView from "./IncomingProjectView";
import { DepartmentProject } from "@/types/organization";

interface IProps {
  departmentProject: DepartmentProject
}
const ProjectOverviewView: FC<IProps> = ({ departmentProject }) => {
  return <>
    <div className="w-full overflow-x-auto flex">
      {departmentProject.all_workgroups.map((workgroup, index) =>
        <Card
          key={`project-${index}`}
          className="mx-4"
          style={{ width: 350 }}
          title={workgroup.workgroup_name}>
          <ProjectStatusPieChart className="w-[180px] h-[180px]" project={workgroup} showComplete={false}/>
          <div className="font-bold">
            Status
            {(workgroup.status1?.trim() ?? '') !== '' && <div className="font-light">
              - {workgroup.status1}
            </div>}
            {(workgroup.status2?.trim() ?? '') !== '' && <div className="font-light">
              - {workgroup.status2}
            </div>}
          </div>
          <ProjectBudgetColumnChart />
        </Card>)}
    </div>
    <div className="my-2"/>
    <div className="grid grid-cols-3 gap-4">

      <ProjectTimeStatusView />
      <ProjectFocusAndWorkloadView className="col-span-2" departmentProject={departmentProject} />

      <h1 className="font-bold text-xl">Incoming Project</h1>
      <IncomingProjectView className="col-span-3" />
    </div>
  </>
}

export default ProjectOverviewView
