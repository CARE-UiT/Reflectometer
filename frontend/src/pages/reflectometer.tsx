import { FC, useEffect } from "react";
import { DrawLineChart } from "../components/DrawLineChart";
import { useParams } from "react-router-dom";
import { Typography, Container, Box, Grid } from "@mui/material";

export const ReflectometerPage: FC = () => {
    const { id } = useParams();

    useEffect(() => console.log(id), [id]);

    return (
        <Container maxWidth="lg" style={{ height: '100vh', display: 'flex', flexDirection: 'column', paddingTop: '80px' }}>
            <Grid container spacing={3} style={{ flex: 1 }}>
                <Grid item xs={12} style={{ height: '100%' }}>
                    <DrawLineChart onPointSelect={(x, y) => console.log(x, y)} />
                </Grid>
            </Grid>
        </Container>
    );
};
