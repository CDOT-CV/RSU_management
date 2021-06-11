import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { ActiveTIMsComponent } from "./active-tims/active-tims.component";
import { InstallationStatusComponent } from "./installation-status/installation-status.component";
import { TotalCountComponent } from "./total-count/total-count.component";

const routes: Routes =[{
    path: 'total_count',
    component: TotalCountComponent
},{
    path: 'active_tims',
    component: ActiveTIMsComponent
}, {
    path: 'installation_status',
    component: InstallationStatusComponent
}
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}