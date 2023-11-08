// nodeLibrary.js
// affilate = [{id: __, Name: ___, Department: ___, Interest: ___, Email: ___, WSU Campus: ___, URL: ___}]

import University from "../../assets/UniversityW.png";
import Entity from "../../assets/EntityW.png";
import Interest from "../../assets/InterestB.png";
import Project from "../../assets/ProjectW.png";
import Publication from "../../assets/PublicationW.png";
import Department from "../../assets/DepartmentW.png";
import Sponsor from "../../assets/SponsorW.png";
import Partner from "../../assets/PartnerW.png";
import Event from "../../assets/EventB.png";
import Scholar from "../../assets/ScholarW.png";
import Journal from "../../assets/JournalW.png";

export let nodesLibrary = [
  // posible root nodes
  {
    id: 0,
    Name: "Universities",
    icon: University,
    expanded: false,
    depth: 0,
    fx: 500,
    fy: 400,
  },
  {
    id: 1,
    Name: "Entities",
    icon: Entity,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  {
    id: 2,
    Name: "Interests",
    icon: Interest,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  {
    id: 3,
    Name: "Projects",
    icon: Project,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  {
    id: 4,
    Name: "Publications",
    icon: Publication,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  {
    id: 5,
    Name: "Departments",
    icon: Department,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  // possible children nodes of Universities
  {
    id: 6,
    Name: "WSU",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 0,
  },
  {
    id: 7,
    Name: "Oregon State",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 0,
  },
  // possible children nodes of Entities
  {
    id: 8,
    Name: "Sponsors",
    icon: Sponsor,
    expanded: false,
    depth: 0,
    parent: 1,
  },
  {
    id: 9,
    Name: "Partners",
    icon: Partner,
    expanded: false,
    depth: 0,
    parent: 1,
  },
  {
    id: 10,
    Name: "Universities Colleges",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 1,
  },
  // possible children nodes of sponsors
  {
    id: 11,
    Name: "Ecol",
    expanded: false,
    depth: 0,
    parent: 8,
  },
  {
    id: 12,
    Name: "NASA",
    expanded: false,
    depth: 0,
    parent: 8,
  },
  {
    id: 13,
    Name: "USDA",

    expanded: false,
    depth: 0,
    parent: 8,
  },
  {
    id: 14,
    Name: "USAID",

    expanded: false,
    depth: 0,
    parent: 8,
  },
  {
    id: 15,
    Name: "NSF",
    expanded: false,
    depth: 0,
    parent: 8,
  },
  // possible children nodes of partners
  {
    id: 16,
    Name: "NM University",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 9,
  },
  {
    id: 17,
    Name: "CA Merced Universiy",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 9,
  },
  {
    id: 18,
    Name: "Cairo Universiy",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 9,
  },
  // possible children nodes of Universities Colleges
  {
    id: 19,
    Name: "WSU(1)",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 10,
  },
  {
    id: 20,
    Name: "UNM",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 10,
  },
  {
    id: 21,
    Name: "UO",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 10,
  },
  {
    id: 22,
    Name: "UI",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 10,
  },
  // possible children nodes of WSU 19
  {
    id: 23,
    Name: "Faculty",

    expanded: false,
    depth: 0,
    parent: 19,
  },
  {
    id: 24,
    Name: "Non-Faculty",

    expanded: false,
    depth: 0,
    parent: 19,
  },
  // possible children nodes for Projects
  {
    id: 25,
    Name: "Project 1",
    expanded: false,
    depth: 0,
    parent: 3,
  },
  {
    id: 26,
    Name: "Project 2",
    expanded: false,
    depth: 0,
    parent: 3,
  },
  // possible children nodes for Publications
  {
    id: 27,
    Name: "Event",
    icon: Event,
    expanded: false,
    depth: 0,
    parent: 4,
  },
  {
    id: 28,
    Name: "Journal Article",
    icon: Journal,
    expanded: false,
    depth: 0,
    parent: 4,
  },
  // possible children nodes for projects 1
  {
    id: 29,
    Name: "Publication",
    icon: Publication,
    expanded: false,
    depth: 0,
    parent: 25,
  },
  {
    id: 30,
    Name: "People",
    icon: Scholar,
    expanded: false,
    depth: 0,
    parent: 25,
  },
  {
    id: 31,
    Name: "Interest",
    icon: Interest,
    expanded: false,
    depth: 0,
    parent: 25,
  },
  // possible children nodes for publication 1
  {
    id: 32,
    Name: "People",
    icon: Scholar,
    expanded: false,
    depth: 0,
    parent: 27,
  },
  {
    id: 35,
    Name: "People",
    icon: Scholar,
    expanded: false,
    depth: 0,
    parent: 28,
  },
  {
    id: 36,
    Name: "Interest",
    icon: Interest,
    expanded: false,
    depth: 0,
    parent: 28,
  },
  {
    id: 37,
    Name: "Entities",
    icon: Entity,
    expanded: false,
    depth: 0,
    parent: 28,
  },
];

export default nodesLibrary;