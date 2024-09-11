import { FC, useEffect, useState } from "react";
import { DrawLineChart } from "../components/DrawLineChart";
import { useParams } from "react-router-dom";
import { Typography, Container, Grid } from "@mui/material";
import axios from "axios";

export const ReflectometerPage: FC = () => {
    const { id } = useParams<{ id: string }>();
    const [loading, setLoading] = useState(true);
    const [sessionExists, setSessionExists] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    // Fetch session data based on the session ID
    useEffect(() => {
        const fetchSession = async () => {
            try {
                const response = await axios.get(`/api/sessions/${id}/exists`);
                if (response.status === 200) {
                    setSessionExists(true);  // Session found
                }
            } catch (error: any) {
                if (error.response && error.response.status === 404) {
                    setSessionExists(false);  // Session not found
                    setErrorMessage(`No session with ID ${id} exists.`);
                } else {
                    setErrorMessage("An error occurred while fetching the session.");
                    console.error(error);
                }
            } finally {
                setLoading(false);  // Finished loading
            }
        };

        if (id) {
            fetchSession();  // Fetch session if ID is present
        }
    }, [id]);

    if (loading) {
        return (
            <Container maxWidth="lg" style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography variant="h6">Loading...</Typography>
            </Container>
        );
    }

    if (!sessionExists) {
        return (
            <Container maxWidth="lg" style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography variant="h6" color="error">{errorMessage}</Typography>
            </Container>
        );
    }

    return (
        <Container maxWidth="lg" style={{ height: '100vh', display: 'flex', flexDirection: 'column', paddingTop: '80px' }}>
            <Grid container spacing={3} style={{ flex: 1 }}>
                <Grid item xs={12} style={{ height: '100%' }}>
                    <DrawLineChart session_id={id!} onPointSelect={(x, y) => console.log(x, y)} />
                </Grid>
            </Grid>
        </Container>
    );
};
