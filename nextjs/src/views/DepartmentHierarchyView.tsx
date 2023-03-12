import DepartmentCard from "@/components/card/department-card";
import { useOrganizationStore } from "@/store";
import { Department } from "@/types/organization";
import { Tree } from "antd";
import { DataNode } from "antd/lib/tree";
import { useRouter } from "next/router";
import { FC, useCallback, useEffect, useState } from "react";

interface IProps {

}

function CreateDepartmentTreeData(departmentList: Department[]): DataNode[] {
  const router = useRouter()
  const { selectedDepartmentId, setSelectedDepartmentId } = useOrganizationStore()
  const handleDepartmentCardClick = useCallback((department: Department) => {
    router.query.departmentId = department.dep_id
    router.replace({ pathname: router.pathname, query: router.query })
    setSelectedDepartmentId(department.dep_id)
  }, [setSelectedDepartmentId, router])
  const departmentDataNodeMapById: Record<string, DataNode> = {}
  const treeData: DataNode[] = []
  departmentList.forEach(department => {
    const cardNode = <DepartmentCard isSelected={department.dep_id === selectedDepartmentId} department={department} onClick={handleDepartmentCardClick} />
    const dataNode = {
      key: department.dep_id,
      title: cardNode,
      children: []
    }
    departmentDataNodeMapById[department.dep_id] = dataNode

    if (department.parent === null) {
      treeData.push(dataNode)
    }
  })

  departmentList.forEach(department => {
    if (department.parent !== null) {
      departmentDataNodeMapById[department.parent].children?.push(departmentDataNodeMapById[department.dep_id])
    }
  })

  return treeData
}

const DepartmentHierachyView: FC<IProps> = ({ }: IProps) => {
  const {
    departmentList
  } = useOrganizationStore()
  const [expandKeyList, setExpandKeyList] = useState<string[]>()

  const expandAllNode = useCallback(() => {
    setExpandKeyList(departmentList.filter(department => department.parent === null).map(department => department.dep_id))
  }, [departmentList, setExpandKeyList])

  useEffect(() => {
    expandAllNode()
  }, [expandAllNode])

  return (
    <Tree
      expandedKeys={expandKeyList}
      className="w-full flex justify-center"
      treeData={CreateDepartmentTreeData(departmentList)} />
  )
}

export default DepartmentHierachyView
