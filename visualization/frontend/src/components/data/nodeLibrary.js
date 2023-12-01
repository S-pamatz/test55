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
    id: 1,
    Name: "Universities",
    icon: University,
    expanded: false,
    depth: 0,
    fx: 500,
    fy: 400,
  },
  {
    id: 2,
    Name: "Entities",
    icon: Entity,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  {
    id: 3,
    Name: "Interests",
    icon: Interest,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  {
    id: 4,
    Name: "Projects",
    icon: Project,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  {
    id: 5,
    Name: "Publications",
    icon: Publication,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  {
    id: 6,
    Name: "Departments",
    icon: Department,
    expanded: false,
    fx: 500,
    fy: 400,
    depth: 0,
  },
  // possible children nodes of Universities
  {
    id: 7,
    Name: "WSU",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 1,
  },
  {
    id: 8,
    Name: "Oregon State",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 1,
  },
  // possible children nodes of Entities
  {
    id: 9,
    Name: "Sponsors",
    icon: Sponsor,
    expanded: false,
    depth: 0,
    parent: 2,
  },
  {
    id: 10,
    Name: "Partners",
    icon: Partner,
    expanded: false,
    depth: 0,
    parent: 2,
  },
  {
    id: 12,
    Name: "Universities Colleges",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 2,
  },
  // possible children nodes of sponsors
  {
    id: 12,
    Name: "Ecol",
    expanded: false,
    depth: 0,
    parent: 9,
  },
  {
    id: 13,
    Name: "NASA",
    expanded: false,
    depth: 0,
    parent: 9,
  },
  {
    id: 14,
    Name: "USDA",

    expanded: false,
    depth: 0,
    parent: 9,
  },
  {
    id: 15,
    Name: "USAID",

    expanded: false,
    depth: 0,
    parent: 9,
  },
  {
    id: 16,
    Name: "NSF",
    expanded: false,
    depth: 0,
    parent: 9,
  },
  // possible children nodes of partners
  {
    id: 17,
    Name: "NM University",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 10,
  },
  {
    id: 18,
    Name: "CA Merced Universiy",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 10,
  },
  {
    id: 19,
    Name: "Cairo Universiy",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 10,
  },
  // possible children nodes of Universities Colleges
  {
    id: 20,
    Name: "WSU(1)",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 11,
  },
  {
    id: 21,
    Name: "UNM",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 11,
  },
  {
    id: 22,
    Name: "UO",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 11,
  },
  {
    id: 23,
    Name: "UI",
    icon: University,
    expanded: false,
    depth: 0,
    parent: 11,
  },
  // possible children nodes of WSU 19
  {
    id: 24,
    Name: "Faculty",

    expanded: false,
    depth: 0,
    parent: 20,
  },
  {
    id: 25,
    Name: "Non-Faculty",

    expanded: false,
    depth: 0,
    parent: 20,
  },
  // possible children nodes for Projects
  {
    id: 26,
    Name: "Project 1",
    expanded: false,
    depth: 0,
    parent: 4,
  },
  {
    id: 27,
    Name: "Project 2",
    expanded: false,
    depth: 0,
    parent: 4,
  },
  // possible children nodes for Publications
  {
    id: 28,
    Name: "Event",
    icon: Event,
    expanded: false,
    depth: 0,
    parent: 5,
  },
  {
    id: 29,
    Name: "Journal Article",
    icon: Journal,
    expanded: false,
    depth: 0,
    parent: 5,
  },
  // possible children nodes for projects 1
  {
    id: 30,
    Name: "Publication",
    icon: Publication,
    expanded: false,
    depth: 0,
    parent: 26,
  },
  {
    id: 31,
    Name: "People",
    icon: Scholar,
    expanded: false,
    depth: 0,
    parent: 26,
  },
  {
    id: 33,
    Name: "Interest",
    icon: Interest,
    expanded: false,
    depth: 0,
    parent: 27,
  },
  // possible children nodes for publication 1
  {
    id: 34,
    Name: "People",
    icon: Scholar,
    expanded: false,
    depth: 0,
    parent: 28,
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