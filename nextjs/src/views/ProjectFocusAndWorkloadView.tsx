import ProjectBudgetColumnChart from "@/components/chart/column/project-budget-column";
import ProjectStatusPieChart from "@/components/chart/pie/project-status-pie";
import { DepartmentProject } from "@/types/organization";
import { Card, Segmented } from "antd";
import { FC, useMemo, useState } from "react";
import { AiFillProject, AiFillSliders } from "react-icons/ai";

interface IProps {
  className?: string
  departmentProject: DepartmentProject
}

const segmentList = [
  {
    label: "Special/Focused Project",
    value: 0,
    icon: <AiFillProject />
  },
  {
    label: "Workload",
    value: 1,
    icon: <AiFillSliders />
  }
]

const ProjectFocusAndWorkloadView: FC<IProps> = ({ className, departmentProject }) => {
  const [selectedTab, setSelectedTab] = useState(0)
  const baseClass = ''
  const parentClass = className === undefined ? baseClass : `${baseClass} ${className}`


  const renderTab = useMemo(() => {
    switch (selectedTab) {
      case 0:
        return <div className="w-full overflow-x-auto flex">
          {departmentProject.focused_projects.map((project, index) =>
            <Card
              key={`project-${index}`}
              className="mr-4 project-horizontal-card"
              style={{ width: 600 }}
              title={project.workgroup_name}
              actions={[
                <div className="font-bold text-black" key={`project-status-${index}`}>
                  Status
                  {(project.status1?.trim() ?? '') !== '' && <div className="font-light">
                    - {project.status1}
                  </div>}
                  {(project.status2?.trim() ?? '') !== '' && <div className="font-light">
                    - {project.status2}
                  </div>}
                </div>
              ]}>
              <ProjectStatusPieChart className="w-[200px] h-[200px]" project={project} showComplete={false} />
              <ProjectBudgetColumnChart />
            </Card>)}
        </div>
      case 1:
        return <>
        </>
      default:
        return <>
        </>
    }
  }, [selectedTab, departmentProject])
  return (
    <div className={parentClass}>
      <Segmented value={selectedTab} options={segmentList} onChange={(v) => setSelectedTab(v as number)} />
      {renderTab}
    </div>
  )
}

export default ProjectFocusAndWorkloadView
