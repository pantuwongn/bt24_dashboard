import dynamic from "next/dynamic";
import { FC } from "react";
import { PieConfig } from '@ant-design/charts'

const Pie = dynamic(() => import("@ant-design/charts").then((m) => m.Pie), { ssr: false })

interface IProps {}

const data: Record<string, any>[] = [
  {
    type: 'Not start',
    value: 8,
  },
  {
    type: 'Delay',
    value: 2,
  },
  {
    type: 'On plan',
    value: 13,
  }
]

const config: PieConfig = {
  data,
  appendPadding: 10,
  angleField: 'value',
  colorField: 'type',
  radius: 0.8,
  width: 180,
  height: 180,
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

const ProjectStatusPieChart: FC<IProps> = () => {
  return (
    <Pie { ...config }/>
  )
}

export default ProjectStatusPieChart
