import dynamic from "next/dynamic";
import { FC } from "react";
import { PieConfig } from '@ant-design/charts'
import { Project } from "@/types/organization";
import { parseProjectStatusPieChart } from "@/functions";

const Pie = dynamic(() => import("@ant-design/charts").then((m) => m.Pie), { ssr: false })

interface IProps {
  className?: string
  project: Project
  showComplete: boolean
}

const ProjectStatusPieChart: FC<IProps> = ({ className, project, showComplete }) => {
  const config: PieConfig = {
    data: parseProjectStatusPieChart(project, showComplete),
    angleField: 'value',
    colorField: 'type',
    radius: 1,
    autoFit: true,
    label: {
      type: 'outer',
      content: '{name} {percentage}',
    },
    interactions: [
      {
        type: 'pie-legend-active',
      },
      {
        type: 'element-active',
      },
    ]
  }
  return <div className={className}>
    <Pie { ...config }/>
  </div>
}

export default ProjectStatusPieChart
