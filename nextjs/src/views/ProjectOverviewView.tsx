import ProjectBudgetColumnChart from "@/components/chart/column/project-budget-column";
import ProjectStatusPieChart from "@/components/chart/pie/project-status-pie";
import { Card } from "antd";
import { FC } from "react";
import ProjectTimeStatusView from "./ProjectTimeStatusView";
import ProjectFocusAndWorkloadView from "./ProjectFocusAndWorkloadView";
import IncomingProjectView from "./IncomingProjectView";

interface IProps { }
const ProjectOverviewView: FC<IProps> = ({ }) => {
  return (
    <div className="grid grid-cols-3 gap-4">
      <Card
        title="4679-Alternator">
        <ProjectStatusPieChart />
        <ProjectBudgetColumnChart />
      </Card>
      <Card
        title="4679-Alternator">
        <ProjectStatusPieChart />
        <ProjectBudgetColumnChart />
      </Card>
      <Card
        title="4679-Alternator">
        <ProjectStatusPieChart />
        <ProjectBudgetColumnChart />
      </Card>

      <ProjectTimeStatusView/>
      <ProjectFocusAndWorkloadView className="col-span-2"/>

      <h1 className="font-bold text-xl">Incoming Project</h1>
      <IncomingProjectView className="col-span-3"/>
    </div>
  )
}

export default ProjectOverviewView
